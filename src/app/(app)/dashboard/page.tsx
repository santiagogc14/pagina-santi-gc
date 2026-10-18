import { Card } from "@/components/ui/card";

export default function DashboardPage() {
  return (
    <Card>
      <h1 className="text-lg font-semibold">Resumen</h1>
      <p className="text-sm text-neutral-500">El presupuesto del mes aparecerá aquí.</p>
    </Card>
  );
}
