appium:
	appium > /dev/null 2>&1 &

ios:
	PLATFORM_NAME=ios \
	DEVICE_NAME="iPhone" \
	PLATFORM_VERSION=26.4.2 \
	UDID=00008110-00000000000000E \
	USE_PREBUILT_WDA=True \
	pytest -v

android:
	pytest -v