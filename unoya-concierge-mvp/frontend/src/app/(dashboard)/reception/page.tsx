import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

export default function ReceptionDashboard() {
  const visitors = [
    { id: 1, name: "Alice Johnson", company: "TechCorp", host: "Jane Doe", arrival: "10:00 AM", status: "expected" },
    { id: 2, name: "Bob Wilson", company: "Global Inc", host: "John Smith", arrival: "10:30 AM", status: "checked_in" },
  ];

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold">Reception Queue</h1>

      <div className="grid grid-cols-1 gap-4">
        {visitors.map((visitor) => (
          <Card key={visitor.id}>
            <CardContent className="flex items-center justify-between p-6">
              <div>
                <div className="text-xl font-semibold">{visitor.name}</div>
                <div className="text-sm text-slate-500">{visitor.company} • Visiting {visitor.host}</div>
              </div>
              <div className="flex items-center gap-4">
                <div className="text-sm">{visitor.arrival}</div>
                <Badge variant={visitor.status === "checked_in" ? "default" : "secondary"}>
                  {visitor.status.replace("_", " ")}
                </Badge>
                {visitor.status === "expected" && (
                  <Button size="sm">Check In</Button>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
