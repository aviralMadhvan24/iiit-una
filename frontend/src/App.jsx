import { Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Warning from "./pages/Warning";
import Forensic from "./pages/Forensic";
import AlertReview from "./pages/AlertReview";
import AlertAction from "./pages/AlertAction";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/warning" element={<Warning />} />
      <Route path="/forensic" element={<Forensic />} />
      <Route path="/review" element={<AlertReview />} />
      <Route path="/action" element={<AlertAction />} />
    </Routes>
  );
}
