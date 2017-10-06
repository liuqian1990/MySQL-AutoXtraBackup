from prepare_env_test_mode.test_check_env import TestModeConfCheck
from general_conf.generalops import GeneralClass
import subprocess
import os
import logging
logger = logging.getLogger(__name__)


class CloneBuildStartServer:
    """
    Class for cloning from git, building server from source and starting test server
    """
    def __init__(self):
        self.git_cmd = GeneralClass().gitcmd

        # Creating needed path here
        t_obj = TestModeConfCheck()
        t_obj.check_test_path(t_obj.testpath)
        self.testpath = t_obj.testpath



    @staticmethod
    def clone_percona_qa(test_path):
        # Clone percona-qa repo for using existing bash scripts
        clone_cmd = "git clone https://github.com/Percona-QA/percona-qa.git {}/percona-qa"
        status, output = subprocess.getstatusoutput(clone_cmd.format(test_path))
        if status == 0:
            logger.debug("percona-qa ready to use")
            return True
        else:
            logger.error("Cloning percona-qa repo failed")
            logger.error(output)
            return False

    @staticmethod
    def clone_ps_server_from_conf(git_cmd, test_path):
        # Clone PS server[the value coming from config file]
        clone_cmd = "git clone {} {}/PS-5.7-trunk"
        status, output = subprocess.getstatusoutput(clone_cmd.format(git_cmd, test_path))
        if status == 0:
            logger.debug("PS cloned ready to build")
            return True
        else:
            logger.error("Cloning PS failed")
            logger.error(output)
            return False

    @staticmethod
    def build_server(test_path):
        # Building server from source
        # For this purpose; I am going to use build_5.x_debug.sh script from percona-qa
        saved_path = os.getcwd()
        # Specify here the cloned PS path; for me it is PS-5.7-trunk
        new_path = "{}/PS-5.7-trunk"
        os.chdir(new_path.format(test_path))
        build_cmd = "{}/percona-qa/build_5.x_debug.sh"
        status, output = subprocess.getstatusoutput(build_cmd.format(test_path))
        if status == 0:
            logger.debug("PS build succeeded")
            os.chdir(saved_path)
            return True
        else:
            logger.error("PS build failed")
            logger.error(output)
            os.chdir(saved_path)
            return False

    @staticmethod
    def get_basedir(test_path):
        # Method for getting PS basedir path
        cmd = 'ls -1td {}/PS* | grep -v ".tar" | grep PS[0-9]'
        status, output = subprocess.getstatusoutput(cmd.format(test_path))
        if status == 0:
            logger.debug("Could get PS basedir path returning...")
            return output
        else:
            logger.error("Could not get PS basedir path failed...")
            logger.error(output)
            return False

    @staticmethod
    def prepare_startup(basedir_path, test_path):
        # Method for calling startup.sh file from percona-qa folder
        saved_path = os.getcwd()
        os.chdir(basedir_path)

        startup_cmd = "{}/percona-qa/startup.sh"
        status, output = subprocess.getstatusoutput(startup_cmd.format(test_path))
        if status == 0:
            logger.debug("Running startup.sh succeeded")
            os.chdir(saved_path)
            return True
        else:
            logger.error("Running startup.sh failed")
            logger.error(output)
            os.chdir(saved_path)
            return False

    @staticmethod
    def start_server(basedir_path):
        # Method for calling start script which is created inside PS basedir
        start_cmd = "{}/start"
        status, output = subprocess.getstatusoutput(start_cmd.format(basedir_path))
        if status == 0:
            logger.debug("Server started!")
            return True
        else:
            logger.error("Server start failed")
            logger.error(output)
            return False