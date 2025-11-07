const parseValue = val => {
  const str = String(val);

  if (str.includes('/')) {
    const [earliest, latest] = str.split('/').map(s => parseInt(s.trim()));
    return { earliest, latest };
  } else if (str.includes('>=')) {
    const earliest = parseInt(str.replace('>=', ''));
    return { earliest }
  } else {
    return { year: parseInt(str)}
  }
}

const parseFull = obj => {
  const earliest = obj.timespans
    .reduce((earliest, ts) => {
      return (earliest && earliest < ts.start) ? earliest : ts.start?.in;
    }, null);

  const latest = obj.timespans
    .reduce((latest, ts) => {
      return (latest && latest > ts.end) ? latest : ts.end?.in;
    }, null);

  return { earliest, latest };
}

const isValue = arg => 
  typeof arg === 'string' || arg instanceof String || !isNaN(arg);

export const parseWhen = arg => {

  if (!arg)
    return null;
  
  const {
    earliest,
    latest,
    year
  } = isValue(arg) ? parseValue(arg) : parseFull(arg);

 let label;


  // Convert to integers and handle the absolute value
  const earliestInt = parseInt(earliest);
  const latestInt = parseInt(latest);

  if (earliestInt && latestInt) {
    const earliestLabel = earliestInt < 0 ? `${Math.abs(earliestInt)} BC` : `AD ${earliestInt}`;
    const latestLabel = latestInt < 0 ? `${Math.abs(latestInt)} BC` : `AD ${latestInt}`;
    label = `${earliestLabel} - ${latestLabel}`;
  } else if (earliestInt) {
    label = earliestInt < 0 ? `after ${Math.abs(earliestInt)} BC` : `after AD ${earliestInt}`;
  } else if (latestInt) {
    label = latestInt < 0 ? `before ${Math.abs(latestInt)} BC` : `before AD ${latestInt}`;
  } else if (year) {
    const yearInt = parseInt(year);
    label = yearInt < 0 ? `${Math.abs(yearInt)} BC` : `AD ${yearInt}`;
  }

  return {
    earliest: earliest || year,
    latest: latest || year,
    year,
    label
  }

}
