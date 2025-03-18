import speedtest

class SpeedTester:
    def __init__(self):
        self.st = speedtest.Speedtest()

    def download_speed(self):
        """Returns the download speed in Mbps."""
        download_speed = self.st.download() / 1_000_000 
        return round(download_speed, 2)

    def upload_speed(self):
        upload_speed = self.st.upload() / 1_000_000
        return round(upload_speed, 2)

    def ping(self):
        server = self.st.get_best_server()
        return round(server['latency'], 2)

    def full_test(self):
        download = self.download_speed()
        upload = self.upload_speed()
        latency = self.ping()

        return {
            "Download Speed (Mbps)": download,
            "Upload Speed (Mbps)": upload,
            "Ping (ms)": latency
        }

if __name__ == "__main__":
    tester = SpeedTester()
    print("Download Speed: ", tester.download_speed(), "Mbps")
    print("Upload Speed: ", tester.upload_speed(), "Mbps")
    print("Ping: ", tester.ping(), "ms")
    print("\nFull Test Results:")
    results = tester.full_test()
    for key, value in results.items():
        print(f"{key}: {value}")
