import * as React from "react";
import { cn } from "@/lib/utils";

export function Input({ className, ...props }: React.ComponentProps<"input">) {
  return (
    <input
      className={cn(
        "h-10 w-full rounded-md border border-neutral-300 bg-white px-3 text-base outline-none focus:ring-2 focus:ring-neutral-400",
        className,
      )}
      {...props}
    />
  );
}
