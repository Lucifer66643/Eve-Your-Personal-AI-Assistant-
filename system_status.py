import time
from take_command import take_command

class SystemHealthMonitor:
    def __init__(self):
        """Initialize the System Health Monitor."""
        self.system_info = self.get_system_info()

    def get_system_info(self):
        """Retrieve basic system information."""
        import platform
        uname = platform.uname()
        return {
            "System": uname.system,
            "Node Name": uname.node,
            "Release": uname.release,
            "Version": uname.version,
            "Machine": uname.machine,
            "Processor": uname.processor
        }

    def get_cpu_usage(self):
        """Get current CPU usage percentage."""
        import psutil
        return psutil.cpu_percent(interval=1)

    def get_memory_usage(self):
        """Get current memory usage details."""
        import psutil
        memory = psutil.virtual_memory()
        return {
            "Total": memory.total,
            "Used": memory.used,
            "Free": memory.free,
            "Percentage": memory.percent
        }

    def get_disk_usage(self):
        """Get current disk usage details."""
        import psutil
        disk = psutil.disk_usage('/')
        return {
            "Total": disk.total,
            "Used": disk.used,
            "Free": disk.free,
            "Percentage": disk.percent
        }

    def get_system_uptime(self):
        """Get system uptime."""
        import psutil
        uptime_seconds = time.time() - psutil.boot_time()
        return time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))

    def check_system_health(self, option):
        """Check system health based on user's choice."""
        if option == "cpu":
            cpu_usage = self.get_cpu_usage()
            print(f"CPU usage is {cpu_usage} percent.")
        
        elif option == "memory":
            memory_usage = self.get_memory_usage()
            print(f"Total memory: {memory_usage['Total'] / (1024 ** 3):.2f} GB, Used: {memory_usage['Used'] / (1024 ** 3):.2f} GB, Free: {memory_usage['Free'] / (1024 ** 3):.2f} GB, Memory usage: {memory_usage['Percentage']} percent.")
        
        elif option == "disk":
            disk_usage = self.get_disk_usage()
            print(f"Total disk space: {disk_usage['Total'] / (1024 ** 3):.2f} GB, Used: {disk_usage['Used'] / (1024 ** 3):.2f} GB, Free: {disk_usage['Free'] / (1024 ** 3):.2f} GB, Disk usage: {disk_usage['Percentage']} percent.")
        
        elif option == "uptime":
            uptime = self.get_system_uptime()
            print(f"System uptime is {uptime}.")
        
        else:
            print("Invalid option, please choose from CPU, memory, disk, or uptime.")

if __name__ == "__main__":
    monitor = SystemHealthMonitor()
    print("What would you like to check? You can say CPU, memory, disk, or uptime.")
    
    option = take_command()
    monitor.check_system_health(option)
