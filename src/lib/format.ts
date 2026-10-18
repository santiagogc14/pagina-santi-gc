const currency = process.env.NEXT_PUBLIC_APP_CURRENCY ?? "COP";

const money = new Intl.NumberFormat("es-CO", {
  style: "currency",
  currency,
  maximumFractionDigits: 0,
});

export function formatMoney(value: number) {
  return money.format(value);
}

export function formatPercent(value: number) {
  return `${Math.round(value)}%`;
}
