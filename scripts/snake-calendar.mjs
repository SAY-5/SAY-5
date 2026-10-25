// Preloaded (node --import) before the generate-snake-animation CLI. The CLI asks GitHub for the
// past year's contribution calendar in one GraphQL query, which GitHub refuses for this account
// from the workflow token ("Resource limits for this query exceeded", every run since 2026-10-19)
// while each half year answers. This answers that one request with two half-year queries merged
// into the same response shape. Levels are recomputed from the year's counts (quartiles of the
// days with contributions), so both halves are shaded on one scale. GitHub computes some days'
// counts per query window, so a few days can read slightly differently than in a one-year query
// (the merged year summed to within 1.2 percent of GitHub's one-year total on 2026-10-25). Every
// other request passes through unchanged.

const realFetch = globalThis.fetch;
const GRAPHQL = 'https://api.github.com/graphql';
const QUERY = `query ($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar { weeks { contributionDays { contributionCount weekday date } } }
    }
  }
}`;
const LEVELS = ['NONE', 'FIRST_QUARTILE', 'SECOND_QUARTILE', 'THIRD_QUARTILE', 'FOURTH_QUARTILE'];
const json = (body) => new Response(JSON.stringify(body), { status: 200, headers: { 'content-type': 'application/json' } });
const day = (d) => d.toISOString().slice(0, 10);

async function calendar(url, init, login) {
  const to = new Date();
  const from = new Date(Date.UTC(to.getUTCFullYear() - 1, to.getUTCMonth(), to.getUTCDate() + 1));
  // Split at a UTC midnight so no day is counted by both halves.
  const mid = new Date(Date.UTC(from.getUTCFullYear(), from.getUTCMonth() + 6, from.getUTCDate()));
  const days = new Map();
  for (const [a, b] of [[from, mid], [mid, to]]) {
    const body = JSON.stringify({ query: QUERY, variables: { login, from: a.toISOString(), to: b.toISOString() } });
    const res = await realFetch(url, { ...init, body });
    if (!res.ok) return res;
    const out = await res.json();
    if (out.errors?.length) return json(out);
    for (const w of out.data.user.contributionsCollection.contributionCalendar.weeks) {
      for (const d of w.contributionDays) {
        const seen = days.get(d.date);
        if (!seen || d.contributionCount > seen.contributionCount) days.set(d.date, d);
      }
    }
  }

  const list = [...days.values()].filter((d) => d.date >= day(from) && d.date <= day(to)).sort((a, b) => a.date.localeCompare(b.date));
  const counts = list.map((d) => d.contributionCount).filter((c) => c > 0).sort((a, b) => a - b);
  const q = (p) => counts[Math.max(0, Math.ceil(p * counts.length) - 1)] ?? 0;
  const [q1, q2, q3] = [q(0.25), q(0.5), q(0.75)];
  const level = (c) => (c === 0 ? 0 : c <= q1 ? 1 : c <= q2 ? 2 : c <= q3 ? 3 : 4);

  const weeks = [];
  for (const d of list) {
    if (!weeks.length || d.weekday === 0) weeks.push({ contributionDays: [] });
    weeks.at(-1).contributionDays.push({ ...d, contributionLevel: LEVELS[level(d.contributionCount)] });
  }
  return json({ data: { user: { contributionsCollection: { contributionCalendar: { weeks } } } } });
}

globalThis.fetch = async (url, init = {}) => {
  if (String(url) !== GRAPHQL || !String(init.body ?? '').includes('contributionCalendar')) return realFetch(url, init);
  return calendar(url, init, JSON.parse(init.body).variables.login);
};
