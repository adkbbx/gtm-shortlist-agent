/** The website field on the start page: one plain text box, labelled for screen readers. */
export function WebsiteField({ value, onChange, disabled, label, placeholder, inputId = 'website' }: {
  value: string; onChange: (value: string) => void; disabled: boolean; label: string; placeholder: string; inputId?: string;
}) {
  return <div className="company-search">
    <input id={inputId} type="text" inputMode="url" autoComplete="url" autoCapitalize="none" spellCheck={false}
      aria-label={label} placeholder={placeholder} value={value} disabled={disabled}
      onChange={event => onChange(event.target.value)} />
  </div>;
}
