using System;
using System.IO;
using System.Text.RegularExpressions;
using System.Diagnostics;

namespace DockerLogToEventLog
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length != 3)
            {
                Console.WriteLine("Usage: DockerLogToEventLog.exe <path_to_log_file> <log_name> <source_name>");
                return;
            }

            string logFilePath = args[0];
            string logName = args[1];
            string sourceName = args[2];

            if (!EventLog.SourceExists(sourceName))
            {
                EventLog.CreateEventSource(sourceName, logName);
            }

            string[] logLines;
            try
            {
                using (FileStream fileStream = new FileStream(logFilePath, FileMode.Open, FileAccess.Read, FileShare.ReadWrite))
                using (StreamReader reader = new StreamReader(fileStream))
                {
                    List<string> lines = new List<string>();
                    while (!reader.EndOfStream)
                    {
                        lines.Add(reader.ReadLine());
                    }
                    logLines = lines.ToArray();
                }
            }
            catch (IOException e)
            {
                Console.WriteLine("An IO exception occurred: " + e.Message);
                return;
            }
            catch (Exception e)
            {
                Console.WriteLine("An exception occurred: " + e.Message);
                return;
            }


            string pattern = @"^\[(?<timestamp>.*?)\]\[(?<source>.*?)\]\[(?<sev_short>.)\] time="".*?"" level=(?<severity>.*?) msg=""(?<message>.*)""";

            foreach (var line in logLines)
            {
                var match = Regex.Match(line, pattern);
                if (match.Success)
                {
                    string timestamp = match.Groups["timestamp"].Value;
                    string source = match.Groups["source"].Value;
                    string severity = match.Groups["severity"].Value;
                    string message = match.Groups["message"].Value;

                    EventLogEntryType entryType = EventLogEntryType.Information;

                    switch (severity)
                    {
                        case "warning":
                            entryType = EventLogEntryType.Warning;
                            break;
                        case "error":
                            entryType = EventLogEntryType.Error;
                            break;
                    }

                    string finalMessage = $"Timestamp: {timestamp} | Source: {source} | Message: {message}";

                    EventLog.WriteEntry(sourceName, finalMessage, entryType);
                }
            }
        }
    }
}