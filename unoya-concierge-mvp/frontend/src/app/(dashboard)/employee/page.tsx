import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Calendar } from "@/components/ui/calendar";

export default function EmployeeDashboard() {
  return (
    <div className="space-y-8">
      <div className="flex justify-between items-end">
        <h1 className="text-3xl font-bold">Welcome back, John</h1>
        <div className="text-slate-500">Employee #1042</div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <Tabs defaultValue="bookings">
            <TabsList className="mb-4">
              <TabsTrigger value="bookings">My Bookings</TabsTrigger>
              <TabsTrigger value="visitors">My Visitors</TabsTrigger>
              <TabsTrigger value="messages">Messages</TabsTrigger>
            </TabsList>
            <TabsContent value="bookings">
              <Card>
                <CardContent className="p-0">
                   <div className="p-6 text-center text-slate-500">No upcoming bookings for today.</div>
                </CardContent>
              </Card>
            </TabsContent>
            <TabsContent value="visitors">
               <Card>
                <CardContent className="p-6">
                  <div className="text-slate-500 text-center">No visitors expected today.</div>
                </CardContent>
              </Card>
            </TabsContent>
            <TabsContent value="messages">
               <Card>
                <CardContent className="p-6">
                   <div className="text-slate-500 text-center">Your inbox is empty.</div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>

        <div>
          <Card>
            <CardHeader>
              <CardTitle>Calendar</CardTitle>
            </CardHeader>
            <CardContent>
              <Calendar mode="single" className="rounded-md border" />
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
