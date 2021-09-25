from subprocess import check_output, PIPE, Popen
import logging

log = logging.getLogger("[NGINX-UI]")

NGINX_EXEC = ""
RELOAD_COMMAND = "{0} -s reload"
CHECK_SYNTAX_COMMAND = "{0} -t"


def check_nginx():
    global NGINX_EXEC
    check_nginx_exec_path_cmd = "which nginx"
    try:
        with Popen(
            check_nginx_exec_path_cmd, stdout=PIPE, stderr=PIPE, shell=True
        ) as process:
            out = process.communicate()
            flag = True
            for output in out:
                output_string = output.decode("utf-8").strip()
                if len(output_string):
                    if "which: no nginx" in output_string:
                        log.warn(f"Found this output for `{reload_nginx_cmd}` => {out}")
                        raise Exception("No nginx exec found")
                    else:
                        NGINX_EXEC = output_string
                        return True
    except Exception as e:
        log.error(f"Failed to reload nginx, {e}")
        raise e

    return False


def reload_nginx():
    reload_nginx_cmd = RELOAD_COMMAND.format(NGINX_EXEC)
    try:
        with Popen(reload_nginx_cmd, stdout=PIPE, stderr=PIPE, shell=True) as process:
            out = process.communicate()
            flag = True
            for output in out:
                output_string = output.decode("utf-8")
                if output_string != "":
                    flag = False

            if flag:
                return True
            log.warn(f"Found this output for `{reload_nginx_cmd}` => {out}")
    except Exception as e:
        log.error(f"Failed to reload nginx, {e}")

    return False


def check_nginx_configuration():
    check_nginx_cmd = CHECK_SYNTAX_COMMAND.format(NGINX_EXEC)
    try:
        with Popen(check_nginx_cmd, stdout=PIPE, stderr=PIPE, shell=True) as process:
            out = process.communicate()
            for output in out:
                output_string = output.decode("utf-8")
                if (
                    "syntax is ok" in output_string
                    and "test is successful" in output_string
                ):
                    return True

            log.warn(f"Found this output for `{check_nginx_cmd}` => {out}")
    except Exception as e:
        log.error(f"Failed to check nginx syntax, {e}")

    return False
