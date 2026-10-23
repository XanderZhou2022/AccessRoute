export function calculateBudget(data, counts) {
  const calls = Object.fromEntries(data.calls.map(c => [c.id, c]));
  let result = { calls: 0, input: 0, output: 0, usd: 0 };
  for (const workflow of data.workflows) {
    const count = counts[workflow.id];
    if (!Number.isInteger(count) || count < 0 || count > 100) throw new RangeError('Invalid action count');
    for (const id of workflow.composition) {
      const call = calls[id];
      result.calls += count;
      result.input += call.input * count;
      result.output += call.output * count;
      result.usd += call.usd * count;
    }
  }
  return result;
}

if (typeof document !== 'undefined') {
  const form = document.querySelector('#budget-form');
  if (form) {
    try {
      const response = await fetch('downloads/service-budget.json');
      if (!response.ok) throw new Error('Budget data unavailable');
      const data = await response.json();
      const keys = ['preferences', 'guidance', 'localization', 'obstacle'];
      const error = document.querySelector('#budget-error');
      const results = document.querySelector('#budget-results');
      const whole = n => n.toLocaleString('en-US');
      function render() {
        const valid = form.checkValidity();
        error.hidden = valid;
        results.hidden = !valid;
        if (!valid) return;
        const values = Object.fromEntries(keys.map(key => [key, Number(form.elements[key].value)]));
        const volume = Number(form.elements.volume.value);
        const result = calculateBudget(data, values);
        document.querySelector('#cost-per-journey').textContent = '$' + result.usd.toFixed(6);
        document.querySelector('#cost-total').textContent = '$' + (result.usd * volume).toFixed(3);
        document.querySelector('#cost-calls').textContent = whole(result.calls);
        document.querySelector('#volume-label').textContent = whole(volume);
        document.querySelector('#cost-tokens').textContent = `${whole(result.input)} input tokens + ${whole(result.output)} output tokens per journey.`;
      }
      form.addEventListener('input', render);
      form.addEventListener('submit', event => { event.preventDefault(); render(); });
      form.querySelectorAll('[data-budget-preset]').forEach(button => button.addEventListener('click', () => {
        const preset = data.journeys[Number(button.dataset.budgetPreset)];
        keys.forEach(key => { form.elements[key].value = preset[key]; });
        render();
      }));
      render();
    } catch {
      document.querySelector('#budget-error').textContent = 'The calculator could not load its data. Use the report tables below or reload the page.';
      document.querySelector('#budget-error').hidden = false;
      document.querySelector('#budget-results').hidden = true;
      form.querySelectorAll('input, button').forEach(control => { control.disabled = true; });
    }
  }
}
