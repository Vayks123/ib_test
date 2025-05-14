#!/bin/bash
set -Eeo pipefail

if [ "$TRADING_MODE" = "paper" ]; then
  printf "Forking :::4000 onto 0.0.0.0:4002\n"
  socat TCP-LISTEN:${IB_PORT},fork TCP:127.0.0.1:4002 &
else
  printf "Forking :::4000 onto 0.0.0.0:4001\n"
  socat TCP-LISTEN:${IB_PORT},fork TCP:127.0.0.1:4001 &
fi

start_xvfb() {
    echo "Starting Xvfb server"
    DISPLAY=:99
    export DISPLAY
    rm -f /tmp/.X99-lock
    Xvfb $DISPLAY -ac -screen 0 1024x768x16 &
    sleep 2
}

start_ibc() {
    echo "Starting IB Gateway"
    TWS_MAJOR_VRSN=$(ls -1 ${HOME}/Jts/ibgateway/.)
    if [ -z "${TWS_MAJOR_VRSN}" ]; then
        echo "Error: Could not determine TWS version"
        exit 1
    fi

    IBC_ARGS=(
        "${TWS_MAJOR_VRSN}" -g
        "--mode=${TRADING_MOD:-paper}"
    )

    if [ -n "${IB_USERNAME}" ] && [ -n "${IB_PASSWORD}" ]; then
        IBC_ARGS+=("--user=${IB_USERNAME}" "--pw=${IB_PASSWORD}")
    else
        echo "Using credentials from config.ini"
    fi

    "${IBC_PATH}/scripts/ibcstart.sh" "${IBC_ARGS[@]}"
}

start_xvfb
start_ibc