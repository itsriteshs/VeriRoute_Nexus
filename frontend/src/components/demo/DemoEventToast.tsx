type DemoEventToastProps = {
  message: string | null;
};

export default function DemoEventToast({ message }: DemoEventToastProps) {
  if (!message) return null;

  return (
    <div className="demo-toast" role="status">
      <span>Demo Event</span>
      <strong>{message}</strong>
    </div>
  );
}
