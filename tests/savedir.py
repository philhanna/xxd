from os import chdir, getcwd


class SaveDirectory:
    """Context manager that saves and restores the current directory"""
    def __enter__(self):
        self.save_cwd = getcwd()

    def __exit__(self, *args):
        chdir(self.save_cwd)
