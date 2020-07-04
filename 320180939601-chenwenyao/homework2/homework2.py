import subprocess, re
import matplotlib.pyplot as plt


class Versions_Time():
    def __init__(self, address):
        self.address = address
        self.versions = self.version()

    def version(self):
        git_tag = subprocess.Popen("git tag", cwd=self.address, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
        git_tag = re.findall('v[0-9].[0-9]', str(git_tag.communicate()[0]))
        git_versions = []
        for i in git_tag:
            if i not in git_versions:
                git_versions.append(i)
        git_versions.pop()
        return git_versions

    def time(self):
        seconds_times = []
        for i in range(0, len(self.versions)):
            git_tag = "git log -1 --pretty=format:\"%ct\" " + self.versions[i]
            git_rev_list = subprocess.Popen(git_tag, cwd=self.address, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
            tag_counts = git_rev_list.communicate()[0]
            if i == 0:
                seconds_times.append(int(tag_counts))
            else:
                seconds_times.append((int(tag_counts) - seconds_times[0])//24//3600)
        seconds_times[0] = 0
        return seconds_times

    def draw_versions(self):
        plt.scatter(self.time(), self.versions)
        plt.title("Version modify date")
        plt.xlabel("date")
        plt.ylabel("version")
        plt.show()


if __name__ == "__main__":
    address = "/Users/cwy19/AppData/linux-stable"
    a = Versions_Time(address)
    print(a.draw_versions())
