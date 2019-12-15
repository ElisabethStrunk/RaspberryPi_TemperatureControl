# Headless setup of a Raspberry Pi (without monitor, keyboard or mouse)

The following instructions are for Windows users.

## Flash Raspbian image to SD card

* Connect the SD card to your PC
* Download the latest version (.zip) of Raspbian: https://www.raspberrypi.org/downloads/<br>
* Flash the image onto your SD card using [Etcher](https://www.balena.io/etcher/).<br>
* Disconnect and reconnect the SD card with your PC. It should be visible in the File Explorer as "boot".

## Set up SSH and WiFi for your Raspberry Pi

* Open a [Git Bash](https://gitforwindows.org/) session and navigate to the _boot_ directory
* Enable SSH:<br>
    Create an ssh file within the _boot_ directory:
    ```bash
    touch ssh
    ```
    This will allow connections via SSH to your Raspberry Pi.
* Set up WiFi:<br>
    Create a _wpa_supplicant.conf_ configuration file within the _boot_ directory:
     ```bash
    touch wpa_supplicant.conf
    ```
    Open the file with an editor (e.g. with [Notepad++](https://notepad-plus-plus.org/)).<br>
    Insert the following lines into _wpa_supplicant.conf_, filling in your data for [alpha-2 country code](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes), network name and network password:
    ```
    country=YOUR_ALPHA-2_COUNTRY_CODE_HERE
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1

    network={
        ssid="YOUR_NETWORK_NAME_HERE"
        psk="YOUR_NETWORK_PASSWORD_HERE"
    }
    ```
    This will cause the Raspberry Pi to connect to the specified WiFi network.

## Boot up your Raspberry Pi

* Remove your SD card from your PC and put it into your Raspberry Pi.
* Connect your Raspberry Pi to the power supply.
* Allow 2-3 minutes during which your Raspberry Pi will boot up and connect to your WiFi.

## Establish an SSH connection between your PC and your Raspberry Pi

* On your PC, make sure that [Download Bonjour Print Services for Windows](https://support.apple.com/kb/dl999?locale=en_US) is installed.
* Make sure that your PC is connected to the same WiFi network that you specified within the _wpa_supplicant.conf_ file.
* Open a Git Bash session and establish an SSH connection with the Raspberry Pi, using the host name _raspberrypi.local_ and the user _pi_:
    ```
    ssh pi@raspberrypi.local
    ```
    The password is _raspberry_.<br>
    Alternatively, use [MobaXTerm](https://mobaxterm.mobatek.net/) or [PuTTY](https://www.putty.org/) to establish the SSH connection.


## Author

**Elisabeth Strunk**<br>
<img src="readme_images/GitHub-Mark-32px.png" width=22> https://github.com/ElisabethStrunk<br>
<img src="readme_images/LI-In-Bug.png" width=22> https://www.linkedin.com/in/elisabeth-strunk/<br>
<br>

## Acknowledgments

* Huge thanks to [Mitch Allen](https://www.linkedin.com/in/mitch-allen-com/) who authored an [article](https://desertbot.io/blog/headless-raspberry-pi-4-ssh-wifi-setup) on setting up ssh and WiFi on a headless Rasperry Pi.