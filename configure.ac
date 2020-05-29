AC_INIT([rhasspy-microphone-pyaudio-hermes], [0.1.0], [mike@rhasspy.org])
AC_CONFIG_MACRO_DIR([m4])
PC_INIT([3.7.0])

dnl ---------------------------------------------------------------------------

AC_PREFIX_DEFAULT([$PWD/.venv])

dnl Template files to write
AC_CONFIG_FILES([Makefile rhasspy-microphone-pyaudio-hermes])

AC_CANONICAL_HOST
AC_PROG_INSTALL
AC_PROG_MKDIR_P
AC_PROG_CC
AC_PROG_CXX

dnl ---------------------------------------------------------------------------

is_virtualenv_enabled=yes
is_dependency_check_enabled=yes

dnl An in-place install does not include Rhasspy Python modules, since they will
dnl be used directly from source.
is_in_place=no

dnl Set architectures based on host CPU
AS_CASE([$host_cpu],
    [armv6l],[
        dnl ARM 32-bit v6 (Pi 1/0)
        docker_arch=armv6
    ],
    [armv7l],[
        dnl ARM 32-bit v7 (Pi 2/3/4)
        docker_arch=armv7
    ],
    [aarch64],[
        dnl ARM 64-bit (Pi 3/4)
        docker_arch=arm64
    ],
    [x86_64],[
        dnl x86_64 compatible
        docker_arch=amd64
    ])

dnl ---------------------------------------------------------------------------

AC_ARG_ENABLE([in-place],
    AS_HELP_STRING([--enable-in-place],
        [do not install Rhasspy Python modules in virtual environment (will be used from source)]))

dnl ---------------------------------------------------------------------------
dnl Python virtual environment
dnl ---------------------------------------------------------------------------

AC_ARG_ENABLE([virtualenv],
    [AS_HELP_STRING([--disable-virtualenv],
        [don't create a Python virtual environment at prefix])])

AC_ARG_VAR([VIRTUALENV_FLAGS], [flags to pass to when creating virtual environment])

dnl In-place install
AS_CASE([$enable_in_place],
    [yes],[is_in_place=yes],
    [no],[is_in_place=no])

dnl ---------------------------------------------------------------------------
dnl Extra Dependency Checks
dnl ---------------------------------------------------------------------------

AC_ARG_ENABLE([dependency-check],
    AS_HELP_STRING([--disable-dependency-check],
        [disable checking for external dependencies]),
    [is_dependency_check_enabled=$enableval])

AS_IF([test "x$is_dependency_check_enabled" = xyes], [

dnl PyAudio requires portaudio.h
AS_IF([test "x$is_pyaudio_enabled" = xyes],
    [
        AC_CHECK_HEADER([portaudio.h], [], [
        AC_MSG_ERROR([portaudio development libary is required for PyAudio microphone (portaudio19-dev package)])
    ])
])

])

dnl ---------------------------------------------------------------------------
dnl Summary
dnl ---------------------------------------------------------------------------

dnl Prefix is NONE for some reason instead of default value
summary_prefix=$prefix
AS_IF([test "x$summary_prefix" = xNONE], [
    summary_prefix=$PWD/.venv
])

AS_ECHO(["
configuration summary:

architecture: ${host_cpu}/${docker_arch}
prefix: ${summary_prefix}
virtualenv: ${is_virtualenv_enabled}
in-place: ${is_in_place}"])

AS_ECHO([""])

dnl ---------------------------------------------------------------------------
dnl Output
dnl ---------------------------------------------------------------------------

AC_SUBST([VIRTUALENV], [$is_virtualenv_enabled])

AC_SUBST([DOCKER_ARCH], [$docker_arch])

AC_SUBST([IN_PLACE], [$is_in_place])

AC_OUTPUT
