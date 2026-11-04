// Contract: return the first n items. n is an integer from 0 through items.length.
export function take(items, n) {
  return items.slice(0, n);
}
