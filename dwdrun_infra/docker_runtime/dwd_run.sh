#!/bin/bash
# POSIX

die() {
    printf '%s\n' "$1" >&2
    exit 1
}

# Initialize all the option variables.
# This ensures we are not contaminated by variables from the environment.
jobModule="none"
runDate="none"

while :; do
    case $1 in
    -h | -\? | --help)
        show_help # Display a usage synopsis.
        exit
        ;;
    --jobModule=?*)
        jobModule=${1#*=} # Delete everything up to "=" and assign the remainder.
        ;;
    --jobModule=) # Handle the case of an empty --file=
        die 'ERROR: "--jobModule" requires a non-empty option argument.'
        ;;
    --runDate=?*)
        runDate=${1#*=} # Delete everything up to "=" and assign the remainder.
        ;;
    --runDate=) # Handle the case of an empty --file=
        die 'ERROR: "--runDate" requires a non-empty option argument.'
        ;;

    -v | --verbose)
        verbose=$((verbose + 1)) # Each -v adds 1 to verbosity.
        ;;
    --) # End of all options.
        shift
        break
        ;;
    -?*)
        printf 'WARN: Unknown option (ignored): %s\n' "$1" >&2
        ;;
    *) # Default case: No more options, so break out of the loop.
        break ;;
    esac
    shift
done

printf "Argument jobModule is %s\n" "$jobModule"
printf "Argument runDate is %s\n" "$runDate"

#docker run -ti --rm test /file.sh abc
#jobModule
docker run --network dwdrunnetwork --env "PYTHONUNBUFFERED=1" --privileged dwdrun:latest --jobModule=$jobModule --runDate=$runDate
