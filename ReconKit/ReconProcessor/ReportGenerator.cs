using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using ReconProcessor.Models;

namespace ReconProcessor.ReportGenerator;

public class ReportGenerator
{
    private string FilePath = "output/results.json";

    public void HTMLReportGenerator()
    {
        ResultModel result = LoadResult();
        StringBuilder sb = new();

        // Build the HTML
        sb.AppendLine("<!DOCTYPE html>");
        sb.AppendLine("<html><head><title>ReconKit Report</title></head><body>");

        // Target info
        sb.AppendLine($"<h1>Scan Report — {result.target}</h1>");
        sb.AppendLine($"<p>Scan Time: {result.scanTime}</p>");

        // Open ports
        sb.AppendLine("<h2>Open Ports</h2>");
        sb.AppendLine("<table>");
        foreach (int port in result.ports.openPorts)
        {
            sb.AppendLine($"<tr><td>{port}</td></tr>");
        }
        sb.AppendLine("</table>");

        // WHOIS
        sb.AppendLine("<h2>WHOIS</h2>");
        sb.AppendLine("<table>");
        sb.AppendLine($"<tr><td>Domain</td><td>{result.whoisModel.domainName}</td></tr>");
        sb.AppendLine($"<tr><td>Registrar</td><td>{result.whoisModel.registrar}</td></tr>");
        sb.AppendLine($"<tr><td>Org</td><td>{result.whoisModel.org}</td></tr>");
        sb.AppendLine($"<tr><td>Country</td><td>{result.whoisModel.country}</td></tr>");
        sb.AppendLine($"<tr><td>Created</td><td>{result.whoisModel.creationDate}</td></tr>");
        sb.AppendLine($"<tr><td>Expires</td><td>{string.Join(", ", result.whoisModel.expirationDate)}</td></tr>");
        sb.AppendLine("</table>");

        // DNS
        sb.AppendLine("<h2>DNS Records</h2>");
        sb.AppendLine("<table>");
        sb.AppendLine($"<tr><td>A</td><td>{string.Join(", ", result.dNSModel.A)}</td></tr>");
        sb.AppendLine($"<tr><td>MX</td><td>{string.Join(", ", result.dNSModel.MX)}</td></tr>");
        sb.AppendLine($"<tr><td>TXT</td><td>{string.Join("<br>", result.dNSModel.TXT)}</td></tr>");
        sb.AppendLine("</table>");

        sb.AppendLine("</body></html>");

        // Write to file
        File.WriteAllText("output/report.html", sb.ToString());
    }
    
    public ResultModel LoadResult()
    {
        try
        {
            string jsonString = File.ReadAllText(FilePath);
            return JsonSerializer.Deserialize<ResultModel>(jsonString)!;
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error loading results: {ex}");
            ResultModel resultModel = new();
            return resultModel;
        }
    }
}