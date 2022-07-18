#!/usr/bin/bash
# /usr/local/bin/bkwww.sh
# Backup web-server
# syslog: journalctl -t BKWWW

# === 0. declarations ===
# consts:
CFG="/usr/local/etc/bkwww.conf"
XCL="/usr/local/etc/bkwww_x.lst"  # excludes (optional; relative to $SRC)
JNAME="BKWWW"  # journalctl tag
LOGDIR="/var/log/bkwww"
OUTLOG="$LOGDIR/out.log"
ERRLOG="$LOGDIR/err.log"
RSYNCLOG="$LOGDIR/rsync.log"
# vars.global:
WWWD="nginx"
SQLD="mariadb"
DAYS=7
WEEKS=5
MONTHS=3
DAILY="day"
WEEKLY="week"
MONTHLY="month"
VERB=2
# vars.local
TODAY=$(date +"%y%m%d")
DST_TODAY=""
PREV=""
SVC_WWW=0
SVC_SQL=0

# === 1. utility ===
log_it() {
    # log to journal/console/logfile/mail
    # $1 - level
    # $2 - msg
    STAMP=$(date +"%Y-%m-%d %H:%M:%S")
    STRING="$STAMP $1: $2"
    if [ -z "$NOLOG_J" ]; then logger -p "$1" -t "$JNAME" "$2"; fi
    if [ -z "$NOLOG_C" ]; then echo "$STRING"; fi
    echo "$STRING" >> "$OUTLOG"
}

log_err() {
    log_it err "$1"
}

log_info() {
    # $1 - verbosity
    # $2 - msg
    [ "$1" -le "$VERB" ] && log_it info "$2"
}

dir_empty() {
    [ -z "$(ls -A "$1")" ] && return 1 || return 0
}

ls_dir() {
    # shellcheck disable=SC2012
    ls -1 "$1" | sort
}

svc_chk() {
    # $1 - service name
    log_info 2 "Check service $1"
    systemctl is-active --quiet "$1"
    retcode=$?
    if [ $retcode -eq 0 ]; then log_info 2 "$1 works"; else log_info 2 "$1 stopped"; fi
    return $retcode
}

svc_do() {
    # try to systemctl service
    # $1 - action
    # $2 - service
    log_info 2 "Try to $1 $2"
    systemctl "$1" "$2"
    retcode=$?
    if [ $retcode -eq 0 ]; then log_info 1 "$2 $1 OK"; else log_err "$2 $1 Fail"; fi
    return $retcode
}

cpal() {
    # $1 - src (related to $DST, like "daily/YYMMDD")
    # $2 - dst (same)
    # @return - None (FIXME:)
    log_info 2 "Copy $1 => $2"
    if ! cp -al "$DST/$1" "$DST/$2" 2>>"$ERRLOG"; then
        log_err "Cannot copy $1 => $2"
        return 1
    fi
}

rotate_dir() {
    # $1 - folder
    # $2 - qty
    # @return - None (FIXME:)
    local QTY=$2
    log_info 2 "Rotate $1 by $2"
    ALL=$(ls_dir "$1" | wc -l)
    if [[ $ALL -gt $QTY ]]; then
        TODEL=$((ALL-QTY))
        for i in $(ls_dir "$1" | head -n "$TODEL"); do
            WHAT2DEL="$1/$i"
            log_info 1 "rmdir $WHAT2DEL"
            rm -rf "$WHAT2DEL"
        done
    else
        log_info 2 "Nothing to do"
    fi
}

# === 2. functions ===
prepare() {
    if [ -z "$SRC" ] || [ -z "$DST" ] || [ -z "$DBNAME" ]; then log_err "Not all variables configured"; return 1; fi
    if [ ! -d "$SRC" ]; then log_err "Source $SRC not found"; return 1; fi
    if [ ! -d "$DST" ]; then log_err "Destination $DST not found"; return 1; fi
    if [ ! -r "$HOME/.my.cnf" ]; then log_err "$HOME/.my.cnf not found"; return 1; fi
    if [ -z "$(ls -A "$DST")" ]; then
        log_info 2 "Create $DST subfolders"
        mkdir "$DST/{$DAILY,$WEEKLY,$MONTHLY}"
    fi
    if [ ! -d "$DST/$DAILY" ]; then log_err "$DST/$DAILY not found"; return 1; fi
    if [ ! -d "$DST/$WEEKLY" ]; then log_err "$DST/$WEEKLY not found"; return 1; fi
    if [ ! -d "$DST/$MONTHLY" ]; then log_err "$DST/$MONTHLY not found"; return 1; fi
    DST_TODAY="$DST/$DAILY/$TODAY"
    svc_chk "$WWWD" && SVC_WWW=1
    svc_chk "$SQLD" && SVC_SQL=1
    log_info 2 "Prepared OK"
}

mk_dir() {
    PREV=$(ls_dir "$DST/$DAILY" | tail -n 1)
    log_info 2 "Creating $DST_TODAY"
    if [ -d "$DST_TODAY" ]; then
        if [ -n "$(ls -A "$DST_TODAY")" ]; then
            log_err "$DST_TODAY already exists and not empty"
            return 1
        fi
    else
        mkdir "$DST_TODAY"
    fi
}

svc_prepare() {
    log_info 2 "Prepare services"
    if [ -n "$SVC_WWW" ]; then
        svc_do stop "$WWWD" || return 1
    fi
    if [ -z "$SVC_SQL" ]; then
        svc_do start "$SQLD" || return 1
    fi
}

svc_restore() {
    log_info 2 "Restore services"
    SQL_NOW=0
    svc_chk "$SQLD" && SQL_NOW=1
    if [ "$SQL_NOW" -ne "$SVC_SQL" ]; then
        [ -z "$SVC_SQL" ] && svc_do stop "$SQLD"
    fi
    WWW_NOW=0
    svc_chk "$WWWD" && WWW_NOW=1
    if [ "$WWW_NOW" -ne "$SVC_WWW" ]; then
        [ -n "$SVC_WWW" ] && svc_do start "$WWWD"
    fi
}

bk_sql() {
    log_info 2 "Backup DB"
    (mysqldump -q "$DBNAME" | zstd > "$DST_TODAY/db.sql.zst") || return 1
    log_info 1 "Backup SQL OK"
}

bk_files() {
    log_info 2 "Backup files"
    if [ -z "$PREV" ]; then
        log_info 2 "Just copy"
        cp -a "$SRC" "$DST_TODAY" || return 1
        log_info 1 "Copy $SRC => $DST_TODAY OK"
    else
        log_info 2 "Rsync..."
        TAIL=$(basename "$SRC")
        [ -f "$XCL" ] && EXCLUDE="--exclude-from=$XCL"
        # archive, same FS, ACL, Xattr, preserve Hardlinks
        rsync -aixAHX --del "$EXCLUDE" --link-dest="../../$PREV/$TAIL" "$SRC/" "$DST_TODAY/$TAIL" > $RSYNCLOG || return 1
        log_info 1 "Rsync $SRC => $DST_TODAY OK"
    fi
}

mk_stat() {
    {
        echo "Sizes, MB:"
        du -sm "$DST"
        du -sm "$DST/$DAILY"
        [ -n "$DST_TODAY" ] && [ -d "$DST_TODAY" ] && du -sm "$DST_TODAY"
    } >> "$OUTLOG"
}

# === 3. ...ly ===
daily() {
    log_info 1 "Daily job"
    (mk_dir &&\
    svc_prepare &&\
    bk_sql &&\
    bk_files &&\
    rotate_dir "$DST/$DAILY" "$DAYS") || RET=1
    svc_restore
    return $RET
}

weekly() {
    if [[ "$(date +%u)" ==  "7" ]]; then
        log_info 2 "Weekly job"
        cpal "$DAILY/$TODAY" "$WEEKLY/$TODAY"
        rotate_dir "$DST/$WEEKLY" "$WEEKS"
    fi
}

monthly() {
    if [ "$(date +%d)" == "01" ]; then
        log_info 2 "Monthly job"
        LAST_WEEKLY=$(ls_dir "$DST/$WEEKLY" | tail -1)
        if [ -n "$LAST_WEEKLY" ]; then
            cpal "$WEEKLY/$LAST_WEEKLY" "$MONTHLY/$LAST_WEEKLY"
            if [ -n "$MONTHS" ]; then
                rotate_dir "$DST/$MONTHLY" "$MONTHS"
            else
                log_err "Bad MONTHS"
            fi
        fi
    fi
}

mail_log() {
    if [ -n "$ODMIN" ]; then mail -s "bkwww $TODAY" "$ODMIN" < "$OUTLOG"; fi
}

# 4. === Main ===
pushd /tmp || exit
if [ ! -r "$CFG" ]; then
    log_err "$CFG not available"
    exit 1
fi
# shellcheck disable=SC1090
source "$CFG"
prepare && (\
    daily &&\
    weekly &&\
    monthly &&\
    mk_stat
    mail_log
)
# log_info 0 "=== the end ==="
popd || exit
