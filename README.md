# npioled

The `npioled` makes it simple to create 1 bit GUI interfaces for the Nano Pi oled screens.

It is platform independent by the use of modular `backend`s modules. This allows to test a GUI on a standard pc (e.g. using the wx backend) while preserving the same screen resolution, color depth (1 bit) and logic as the nano pi.

It integrates utility modules to draw advanced graphics using the matplotlib library and pixel perfect graphics via the PIL library.

The main loop in is full control of the application.

## input mapping

On the wx backend, the `QWE` keys are mapped to the left, center and right buttons. In the nano pi, the raw GPIO inputs are read. An event based approach would be more efficient but the library seems buggy when using events (all the events are only reported for left button pin). See https://github.com/friendlyarm/WiringNP for the C library exposing nano pi board pins.

## color convention

The convention is to use white-on-black graphics. The `backend.invert` method must be used whenever the opposite color scheme is needed.

## Dependencies (nano pi)

On ubuntu:

```
sudo apt-get install python-smbus python-pil python-matplotlib python-numpy python2-psutil
```

On archlinux:

```
sudo pacman -S python2 python2-imaging freetype2 ttf-dejavu python2-psutil python2-numpy python2-matplotlib
```

When using a custom system image, the GPIO python bindings should be installed manually. Check out https://github.com/chainsx/RPi.GPIO.NP .
