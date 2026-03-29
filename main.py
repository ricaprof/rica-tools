from monitor_app import MonitorApp

def main():
    app = MonitorApp()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nEncerrando o monitoramento...")
        pass

if __name__ == "__main__":
    main()