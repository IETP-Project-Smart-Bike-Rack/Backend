import { useState, React} from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faParking, faBicycle } from '@fortawesome/free-solid-svg-icons';
import Profile from "./profile";
const Dashboard = () => {
  const [isSidebarExpanded, setIsSidebarExpanded] = useState(false);
  const [selectedSection, setSelectedSection] = useState("Dashboard");

  const toggleSidebar = () => {
    setIsSidebarExpanded(!isSidebarExpanded);
  };

  const data = [
    { title: "Total Income", value: "$12,487", icon: "💰" },
    { title: "Active Spaces", value: "73%", icon: "🚗" },
    { title: "Violations", value: "6", icon: "⚠️" },
    { title: "Reported Issues", value: "12", icon: "🔧" },
  ];

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <aside
        className={`${
          isSidebarExpanded ? "w-64" : "w-20"
        } bg-gray-800 text-white h-full transition-all duration-300`}
      >
        {/* Toggle Button */}
        <div
          className="flex items-center justify-between p-4 cursor-pointer"
          onClick={toggleSidebar}
        >
          <span className="text-xl font-bold">{isSidebarExpanded ? "Menu" : "☰"}</span>
        </div>

        {/* Navigation Links */}
        <ul className="mt-4 space-y-4">
          <li
            className="flex items-center space-x-4 p-4 hover:bg-gray-700 cursor-pointer"
            onClick={() => setSelectedSection("Available Parking Slots")}
          >
            <FontAwesomeIcon icon={faParking} className="text-white text-2xl" />
            {isSidebarExpanded && <span>Available Parking Slots</span>}
          </li>
          <li
            className="flex items-center space-x-4 p-4 hover:bg-gray-700 cursor-pointer"
            onClick={() => setSelectedSection("Your Slot")}
          >
            <FontAwesomeIcon icon={faBicycle} className="text-white text-2xl" />
            {isSidebarExpanded && <span>Your Slot</span>}
          </li>
          <li
            className="flex items-center space-x-4 p-4 hover:bg-gray-700 cursor-pointer"
            onClick={() => setSelectedSection("Settings")}
          >
            <span className="text-2xl">⚙️</span>
            {isSidebarExpanded && <span>Settings</span>}
          </li>
        </ul>
      </aside>

      {/* Main Dashboard Content */}
      <div className="flex-1 bg-gray-100">
        {/* Header */}
        <header className="bg-white shadow p-4">
          <h1 className="text-xl font-bold">{selectedSection}</h1>
        </header>

        {/* Dynamic Content */}
        <div className="p-6">
          {selectedSection === "Dashboard" && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {data.map((item, index) => (
                <div
                  key={index}
                  className="bg-white shadow rounded-lg p-4 flex items-center space-x-4"
                >
                  <span className="text-3xl">{item.icon}</span>
                  <div>
                    <h2 className="text-gray-600">{item.title}</h2>
                    <p className="text-xl font-bold">{item.value}</p>
                  </div>
                </div>
              ))}
            </div>
          )}

          {selectedSection === "Available Parking Slots" && (
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-2xl font-bold mb-4">Available Parking Slots</h2>
              <p>Currently, there are 25 parking slots available for use.</p>
              <p className="mt-2 text-gray-600">Check back later for updates!</p>
            </div>
          )}

          {selectedSection === "Your Slot" && (
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-2xl font-bold mb-4">Your Slot</h2>
              <p>Your bike is parked in slot <strong>#42</strong>.</p>
              <p className="mt-2 text-gray-600">Time parked: 1 hour, 30 minutes.</p>
            </div>
          )}

          {selectedSection === "Settings" && (
      
              <Profile/>
         
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
