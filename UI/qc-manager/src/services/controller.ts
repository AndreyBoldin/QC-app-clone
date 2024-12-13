export function getBarsData(dataList: object[]) {
  const categories: string[] = []
  const counts: Record<string, number> = {}

  dataList.forEach((data) => {
    const group = (data as { Group: string }).Group
    if (!categories.includes(group)) {
      categories.push(group)
      counts[group] = 0
    }
    counts[group]++
  })

  return { categories, counts }
}