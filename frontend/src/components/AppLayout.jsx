import Header from "./Header";

export default function AppLayout({ children, headerProps }) {
  return (
    <div className="min-h-screen bg-background-dark text-white flex flex-col">
      <Header {...headerProps} />
      <main className="flex-1 overflow-auto">
        {children}
      </main>
    </div>
  );
}
