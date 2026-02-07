export default function Footer({ children }) {
  return (
    <footer className="border-t border-white/10 bg-background-dark/50 px-6 py-4 flex justify-end gap-4">
      {children}
    </footer>
  );
}
