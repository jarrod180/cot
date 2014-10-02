#!/usr/bin/env python
#
# check_and_install_helpers.py - installer helper script for COT package
#
# October 2014, Glenn F. Matthews
#
# See the COPYRIGHT.txt file at the top-level directory of this distribution
# and at https://github.com/glennmatthews/cot/blob/master/COPYRIGHT.txt.
#
# This file is part of the Common OVF Tool (COT) project.
# It is subject to the license terms in the LICENSE.txt file found in the
# top-level directory of this distribution and at
# https://github.com/glennmatthews/cot/blob/master/LICENSE.txt. No part
# of COT, including this file, may be copied, modified, propagated, or
# distributed except according to the terms contained in the LICENSE.txt file.

import distutils.spawn
from distutils.version import StrictVersion
import os
import os.path
import shutil
import subprocess
import sys

import COT.helper_tools
from COT.helper_tools import HelperNotFoundError
from COT.cli import confirm, confirm_or_die

# Look for various package managers:
PORT = distutils.spawn.find_executable('port')
APT_GET = distutils.spawn.find_executable('apt-get')

def check_qemu_and_vmdktool():
    print("Checking for qemu-img executable...")
    try:
        qemu_version = COT.helper_tools.get_qemu_img_version()
    except HelperNotFoundError:
        COT.cli.confirm_or_die("qemu-img not found. Try to install it?")
        if PORT:
            subprocess.check_call(['port', 'install', 'qemu'])
        elif APT_GET:
            subprocess.check_call(['apt-get', 'install', 'qemu'])
        else:
            exit("Not sure how to install QEMU without 'port' or 'apt-get'!\n"
                 "Please install QEMU before proceeding.\n"
                 "See http://en.wikibooks.org/wiki/QEMU/Installing_QEMU")
        qemu_version = COT.helper_tools.get_qemu_img_version()

    print("installed qemu version is {0}".format(qemu_version))

    if qemu_version >= StrictVersion("2.1.0"):
        print("vmdktool is not required")
        return

    print("Checking for vmdktool executable...")

    if not distutils.spawn.find_executable('vmdktool'):
        confirm_or_die("vmdktool not found. Try to install it?")
        if PORT:
            subprocess.check_call(['port', 'install', 'vmdktool'])
        elif APT_GET:
            # We don't have vmdktool in apt yet but we can install it manually:
            # vmdktool requires zlib1g-dev
            subprocess.check_call(['apt-get', 'install', 'zlib1g-dev'])
            try:
                # Get the source
                subprocess.check_call(['wget',
                                       'http://people.freebsd.org/~brian/'
                                       'vmdktool/vmdktool-1.4.tar.gz'])
                subprocess.check_call(['tar', 'zxf', 'vmdktool-1.4.tar.gz'])
                # vmdktool doesn't build cleanly under linux without
                # modifying the CFLAGS:
                env = os.environ.copy()
                env["CFLAGS"] = "-D_GNU_SOURCE"
                subprocess.check_call(['make', '--directory', 'vmdktool-1.4'],
                                      env=env)
                if not os.path.exists('/usr/local/man/man8'):
                    os.makedirs('/usr/local/man/man8', 0755)
                subprocess.check_call(['make', '--directory', 'vmdktool-1.4',
                                       'install'])
            finally:
                if os.path.exists('vmdktool-1.4.tar.gz'):
                    os.remove('vmdktool-1.4.tar.gz')
                if os.path.exists('vmdktool-1.4'):
                    shutil.rmtree('vmdktool-1.4')
        else:
            exit("Not sure how to install vmdktool, sorry!\n"
                 "See http://www.freshports.org/sysutils/vmdktool/")

    print("vmdktool is available")
    return


def check_fatdisk():
    if ((not distutils.spawn.find_executable('fatdisk')) and
        confirm("Optional dependency 'fatdisk' not found. "
                "Try to install it?")):
        if PORT:
            subprocess.check_call(['port', 'install', 'fatdisk'])
        elif sys.platform == 'linux2':
            subprocess.check_call(['wget', '-O', 'fatdisk.zip',
                    'https://github.com/goblinhack/fatdisk/archive/master.zip'])
            subprocess.check_call(['unzip', 'fatdisk.zip'])
            subprocess.check_call(['./RUNME'], cwd='fatdisk-master')
            shutil.copy2('fatdisk-master/fatdisk', '/usr/local/bin/fatdisk')
        else:
            print("Not sure how to install fatdisk, sorry!\n"
                  "See https://github.com/goblinhack/fatdisk")

    if distutils.spawn.find_executable('fatdisk'):
        print("fatdisk is available")
    else:
        print("fatdisk (optional dependency) not installed")
    return

def check_mkisofs():
    if ((not distutils.spawn.find_executable('mkisofs')) and
        confirm("Optional dependency 'mkisofs' not found. "
                "Try to install it?")):
        if PORT:
            subprocess.check_call(['port', 'install', 'cdrtools'])
        else:
            print("Not sure how to install mkisofs, sorry!\n"
                  "See http://cdrecord.org/")

    if distutils.spawn.find_executable('mkisofs'):
        print("mkisofs is available")
    else:
        print("mkisofs (optional dependency) not installed")
    return

def check_ovftool():
    if distutils.spawn.find_executable('ovftool'):
        print("ovftool is available")
    else:
        print("ovftool (optional dependency) not installed.\n"
              "See https://www.vmware.com/support/developer/ovf/")
    return

def main():
    print("Checking for required and optional helper programs...")
    if sys.platform == 'darwin' and not PORT:
        confirm_or_die("It appears you are running on a Mac but "
                       "do not have MacPorts installed.\n"
                       "If you've already installed all helper programs "
                       "that COT needs, this is not a problem.\n"
                       "If any helpers are missing, we could use MacPorts "
                       "to automatically install them for you... "
                       "if it were installed!\n"
                       "See https://www.macports.org/\n"
                       "Continue?")
    elif sys.platform == 'linux2' and not APT_GET:
        confirm_or_die("It appears you are running on a Linux that doesn't "
                       "have 'apt-get' capability.\n"
                       "If you've already installed all helper programs "
                       "that COT needs, this is not a problem.\n"
                       "Continue?")

    check_qemu_and_vmdktool()
    check_fatdisk()
    check_mkisofs()
    check_ovftool()

if __name__ == "__main__":
    main()
