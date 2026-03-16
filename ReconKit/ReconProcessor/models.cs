using System.Text.Json.Serialization;

namespace ReconProcessor.Models;

public class ConfigSettings
{
    [JsonPropertyName("remote_host")]
    public string remoteHost { get; set; } = string.Empty;
    [JsonPropertyName("start_port")]
    public int startPort { get; set; } = 1;
    [JsonPropertyName("end_port")]
    public int endPort { get; set; } = 1;
    [JsonPropertyName("max_concurrent")]
    public int max_concurrent { get; set; } = 500;
}

public class PortModel
{
    [JsonPropertyName("open_ports")]
    public List<int> openPorts { get; set; } = [];
    [JsonPropertyName("nmap_output")]
    public string nmapOutput { get; set; } = string.Empty;
}

public class WhoisModel
{
    [JsonPropertyName("domain_name")]
    public string domainName { get; set; } = string.Empty;
    [JsonPropertyName("registrar")]
    public string registrar { get; set; } = string.Empty;
    [JsonPropertyName("registrar_url")]
    public string registrarUrl { get; set; } = string.Empty;
    [JsonPropertyName("whois_server")]
    public string whoisServer { get; set; } = string.Empty;
    [JsonPropertyName("updated_date")]
    public string updatedDate { get; set; } = string.Empty;
    [JsonPropertyName("creation_date")]
    public string creationDate { get; set; } = string.Empty;
    [JsonPropertyName("expiration_date")]
    public List<string> expirationDate { get; set; } = [];
    [JsonPropertyName("name_servers")]
    public List<string> nameServers { get; set; } = [];
    [JsonPropertyName("status")]
    public List<string> status { get; set; } = [];
    [JsonPropertyName("emails")]
    public List<string> emails { get; set; } = [];
    [JsonPropertyName("dnssec")]
    public string dnssec { get; set; } = string.Empty;
    [JsonPropertyName("org")]
    public string org { get; set; } = string.Empty;
    [JsonPropertyName("country")]
    public string country { get; set; } = string.Empty;
}

public class DNSModel
{
    [JsonPropertyName("A")]
    public List<string> A { get; set; } = [];
    [JsonPropertyName("MX")]
    public List<string> MX { get; set; } = [];
    [JsonPropertyName("TXT")]
    public List<string> TXT { get; set; } = [];
}

public class ResultModel
{
    [JsonPropertyName("target")]
    public string target { get; set; } = string.Empty;
    [JsonPropertyName("scan_time")]
    public string scanTime { get; set; } = string.Empty;
    [JsonPropertyName("ports")]
    public PortModel ports { get; set; } = new();
    [JsonPropertyName("whois")]
    public WhoisModel whoisModel { get; set; } = new();
    [JsonPropertyName("dns")]
    public DNSModel dNSModel { get; set; } = new();
}
