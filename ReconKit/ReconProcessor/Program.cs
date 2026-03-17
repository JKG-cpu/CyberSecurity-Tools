using System.Text.Json;
using System.Text.Json.Nodes;
using ReconProcessor.Models;
using ReconProcessor.ReportGenerator;

public class ConfigLoader
{
    private string FilePath = "config/config.json";

    public void Main()
    {
        ConfigSettings configSettings = LoadConfigSettings();
        bool isValid = CheckValidSettings(configSettings);

        if (!isValid)
        {
            Environment.Exit(1);
        }
        else
        {
            Environment.Exit(0);
        }
    }

    private bool CheckValidSettings(ConfigSettings configSettings)
    {
        // Host
        if (configSettings.remoteHost == string.Empty)
        {
            Console.WriteLine($"Remote host is empty. {configSettings.remoteHost}");
            return false;
        }

        // Ports
        if (configSettings.startPort < 0)
        {
            Console.WriteLine("Start Port is less than 0.");
            return false;
        }

        if (configSettings.endPort < 0 || configSettings.endPort < configSettings.startPort)
        {
            Console.WriteLine("End port is less than the start port OR it is less than 0.");
            return false;
        }

        // Concurrents
        if (configSettings.max_concurrent <= 0)
        {
            Console.WriteLine("You cannot have concurrent amount <= 0.");
            return false;
        }

        return true;
    }

    private ConfigSettings LoadConfigSettings()
    {
        ConfigSettings model = new();

        try
        {
            string config = File.ReadAllText(FilePath);
            model = JsonSerializer.Deserialize<ConfigSettings>(config)!;
            Console.WriteLine(model);
            return model;
        }
        catch (FileNotFoundException)
        {
            Console.WriteLine($"Could not load data from {FilePath}");
        }

        return model;
    }
}

public class Program
{
    public static void Main(string[] args)
    {
        if (args.Length == 0)
        {
            Console.WriteLine("No mode specified. Use --report or --config");
            Environment.Exit(1);
        }

        if (args[0] == "--config")
        {
            ConfigLoader configLoader = new();
            configLoader.Main();
        }
        else if (args[0] == "--report")
        {
            ReportGenerator reportGenerator = new();
            reportGenerator.HTMLReportGenerator();
        }
        else
        {
            Console.WriteLine($"Unknown Argument: {args[0]}");
            Environment.Exit(1);
        }
    }
}