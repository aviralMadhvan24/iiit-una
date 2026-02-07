export default function PageContainer({ children }) {
  return (
    <div className="px-4 sm:px-8 py-6 max-w-[1600px] mx-auto w-full">
      {children}
    </div>
  );
}
