import React from "react";
import Link from "next/link";
import { LayoutDashboard, Users, DoorOpen, Calendar, MessageSquare, Monitor } from "lucide-react";

const Sidebar = () => {
  const links = [
    { name: "Admin", href: "/admin", icon: LayoutDashboard },
    { name: "Employee", href: "/employee", icon: Calendar },
    { name: "Reception", href: "/reception", icon: Users },
    { name: "AI Totem", href: "/totem", icon: Monitor },
  ];

  return (
    <div className="w-64 h-screen bg-slate-950 text-white p-4 flex flex-col border-r border-slate-800">
      <div className="text-xl font-bold mb-8 px-2">UNOYA AI</div>
      <nav className="flex-1 space-y-2">
        {links.map((link) => (
          <Link
            key={link.name}
            href={link.href}
            className="flex items-center gap-3 px-4 py-2 rounded-lg hover:bg-slate-900 transition-colors"
          >
            <link.icon size={20} />
            <span>{link.name}</span>
          </Link>
        ))}
      </nav>
    </div>
  );
};

export default Sidebar;
