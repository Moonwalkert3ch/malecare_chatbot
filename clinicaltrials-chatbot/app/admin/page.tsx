"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Download, RefreshCw, Trash2 } from "lucide-react";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface StatsData {
  total_sessions: number;
  completed_sessions: number;
  total_messages: number;
  total_trials_found: number;
  cancer_types: Record<string, number>;
  locations: Record<string, number>;
  age_groups: Record<string, number>;
  last_updated: string;
}

export default function AdminDashboard() {
  const [stats, setStats] = useState<StatsData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchStats = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${API_BASE_URL}/admin/stats`);
      if (!response.ok) {
        throw new Error("Failed to fetch statistics");
      }
      const data = await response.json();
      setStats(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  const downloadCSV = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/admin/export-csv`);
      if (!response.ok) {
        throw new Error("Failed to export CSV");
      }
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `chatbot_usage_stats_${new Date().toISOString().split('T')[0]}.csv`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to download CSV");
    }
  };

  const clearStats = async () => {
    if (!confirm("Are you sure you want to clear all usage statistics? This cannot be undone!")) {
      return;
    }
    
    try {
      const response = await fetch(`${API_BASE_URL}/admin/clear-stats`, {
        method: "POST",
      });
      if (!response.ok) {
        throw new Error("Failed to clear statistics");
      }
      
      alert("Statistics cleared successfully!");
      fetchStats();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to clear statistics");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Admin Dashboard</h1>
          <p className="text-gray-600">Chatbot Usage Statistics</p>
        </div>

        <div className="mb-6 flex gap-3">
          <Button onClick={fetchStats} disabled={loading}>
            <RefreshCw className="mr-2 h-4 w-4" />
            Refresh Stats
          </Button>
          <Button onClick={downloadCSV} variant="outline">
            <Download className="mr-2 h-4 w-4" />
            Download CSV for Google Sheets
          </Button>
          <Button onClick={clearStats} variant="destructive">
            <Trash2 className="mr-2 h-4 w-4" />
            Clear All Data
          </Button>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            {error}
          </div>
        )}

        {loading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">Loading statistics...</p>
          </div>
        )}

        {stats && !loading && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
            <Card>
              <CardHeader>
                <CardTitle className="text-2xl">{stats.total_sessions}</CardTitle>
                <CardDescription>Total Sessions</CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-2xl">{stats.completed_sessions}</CardTitle>
                <CardDescription>Completed Sessions</CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-2xl">{stats.total_messages}</CardTitle>
                <CardDescription>Total Messages</CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-2xl">{stats.total_trials_found}</CardTitle>
                <CardDescription>Trials Found</CardDescription>
              </CardHeader>
            </Card>
          </div>
        )}

        {stats && !loading && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Cancer Types</CardTitle>
                <CardDescription>Distribution of cancer types searched</CardDescription>
              </CardHeader>
              <CardContent>
                {Object.keys(stats.cancer_types).length === 0 ? (
                  <p className="text-gray-500 text-sm">No data yet</p>
                ) : (
                  <div className="space-y-2">
                    {Object.entries(stats.cancer_types)
                      .sort(([, a], [, b]) => b - a)
                      .map(([type, count]) => (
                        <div key={type} className="flex justify-between items-center">
                          <span className="text-sm font-medium">{type}</span>
                          <span className="text-sm text-gray-600">{count}</span>
                        </div>
                      ))}
                  </div>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Locations</CardTitle>
                <CardDescription>Geographic distribution of users</CardDescription>
              </CardHeader>
              <CardContent>
                {Object.keys(stats.locations).length === 0 ? (
                  <p className="text-gray-500 text-sm">No data yet</p>
                ) : (
                  <div className="space-y-2">
                    {Object.entries(stats.locations)
                      .sort(([, a], [, b]) => b - a)
                      .slice(0, 10)
                      .map(([location, count]) => (
                        <div key={location} className="flex justify-between items-center">
                          <span className="text-sm font-medium">{location}</span>
                          <span className="text-sm text-gray-600">{count}</span>
                        </div>
                      ))}
                  </div>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Age Groups</CardTitle>
                <CardDescription>Age distribution of users</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {Object.entries(stats.age_groups).map(([group, count]) => (
                    <div key={group} className="flex justify-between items-center">
                      <span className="text-sm font-medium">{group}</span>
                      <span className="text-sm text-gray-600">{count}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <h3 className="font-semibold text-blue-900 mb-2">How to use:</h3>
          <ol className="list-decimal list-inside space-y-1 text-sm text-blue-800">
            <li>Click "Download CSV for Google Sheets" to export the data</li>
            <li>Open Google Sheets</li>
            <li>Go to File → Import → Upload tab</li>
            <li>Drag and drop the downloaded CSV file</li>
            <li>Choose "Create new spreadsheet" and click "Import data"</li>
          </ol>
        </div>
      </div>
    </div>
  );
}
