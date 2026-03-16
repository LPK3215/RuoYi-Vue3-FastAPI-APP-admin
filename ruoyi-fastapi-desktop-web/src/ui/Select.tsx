import clsx from 'clsx'
import type { SelectHTMLAttributes } from 'react'

export type SelectProps = SelectHTMLAttributes<HTMLSelectElement> & {
  label?: string
}

export function Select({ className, label, children, ...props }: SelectProps) {
  return (
    <label className={clsx('ds-field', className)}>
      {label ? <span className="ds-label">{label}</span> : null}
      <select className="ds-select" {...props}>
        {children}
      </select>
    </label>
  )
}

