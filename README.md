<div align="center">

<a href="https://github.com/SAY-5">
<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=30&duration=3200&pause=900&color=4AF0C0&center=true&vCenter=true&width=780&lines=Sai+Asish+Yamani;Software+Engineer;Distributed+systems+%C2%B7+low-latency+infra+%C2%B7+databases" alt="header" />
</a>

<br/>

<p>
  <a href="mailto:saiasish.cnp@gmail.com"><img src="https://img.shields.io/badge/email-saiasish.cnp%40gmail.com-4AF0C0?style=flat-square&labelColor=07080A&logo=maildotru&logoColor=4AF0C0" /></a>
  <a href="https://github.com/SAY-5"><img src="https://img.shields.io/badge/github-SAY--5-E8EAED?style=flat-square&labelColor=07080A&logo=github&logoColor=E8EAED" /></a>
  <a href="https://www.linkedin.com/in/saiasishy/"><img src="https://img.shields.io/badge/linkedin-saiasishy-0EA5E9?style=flat-square&labelColor=07080A&logo=linkedin&logoColor=0EA5E9" /></a>
  <a href="https://sayportfolio.vercel.app/"><img src="https://img.shields.io/badge/portfolio-sayportfolio.vercel.app-F0A04A?style=flat-square&labelColor=07080A&logo=vercel&logoColor=F0A04A" /></a>
</p>

</div>

---

### About

I build systems that shouldn't break — and when they do, I want to know *why* in under a millisecond.
Most of my work lives at the seams: low-latency network paths, partitioned storage, real-time pipelines,
and the observability that tells you what actually happened. I lean toward C++, Go, and Rust when it
matters, and TypeScript or Python when shipping fast matters more.

### Currently shipping

```txt
→  SpatialPathDB    Hilbert-partitioned Postgres. 2.5× faster viewport queries across 42M nuclei.
→  Netlat-Analyser  TCP latency + retransmit anomaly detection from pcap. Prometheus, Grafana, k8s.
→  Sigma Terminal   Bloomberg-style market terminal — canvas candlesticks, WebSocket quotes, AI research.
→  Sentinel         Code-safety platform catching secrets and CVEs before they ship.
```

### Selected projects

<table>
<tr>
<td width="50%" valign="top">

#### [SpatialPathDB](https://github.com/SAY-5/SpatialPathDB)

Hilbert-partitioned PostgreSQL storage for digital pathology. Viewport queries **2.5× faster**, cold cache **9.1× faster**. Benchmarked on 42M nuclei across 29 TCGA slides with 89% partition-pruning.

<sub>`Python` · `PostgreSQL` · `PostGIS` · `Hilbert`</sub>

</td>
<td width="50%" valign="top">

#### [Netlat-Analyser](https://github.com/SAY-5/Netlat-Analyser)

pcap analyzer for TCP latency and retransmissions. Three-way RTT measurement, EWMA-based deviation detection, Prometheus metrics, Grafana dashboard, k8s DaemonSet.

<sub>`Python` · `Prometheus` · `Grafana` · `Kubernetes`</sub>

</td>
</tr>
<tr>
<td width="50%" valign="top">

#### [Sigma Terminal](https://github.com/SAY-5/sigma-terminal)

Bloomberg-style financial terminal. Real-time WebSocket quotes, hand-rolled candlestick canvas, 15+ technical indicators, and Claude-powered equity research.

<sub>`Next.js` · `WebSocket` · `Canvas` · `Claude API`</sub>

</td>
<td width="50%" valign="top">

#### [QUIC CDN Simulator](https://github.com/SAY-5/Video-Streaming-CDN-Simulator-with-QUIC-Transport)

Go simulator benchmarking HTTP/3 (QUIC) vs HTTP/2 (TCP) for video CDN workloads. Models packet loss, HOL blocking, ARC caching, and adaptive bitrate. Docker/netem ground-truth mode.

<sub>`Go` · `QUIC` · `netem` · `Docker`</sub>

</td>
</tr>
<tr>
<td width="50%" valign="top">

#### [Sentinel](https://github.com/SAY-5/Sentinel)

Catches secrets, vulnerabilities, and unsafe patterns before they ship. Static analysis meets runtime checks — plugs into CI.

<sub>`TypeScript` · `Static Analysis`</sub>

</td>
<td width="50%" valign="top">

#### [Cubit Streaming](https://github.com/SAY-5/cubit-streaming-system)

Low-latency video streaming pipeline for biomedical microscope cameras. Built in C++ for real-time acquisition and delivery.

<sub>`C++` · `GStreamer` · `RTP`</sub>

</td>
</tr>
</table>

### Stack

<p align="left">
<img src="https://skillicons.dev/icons?i=cpp,go,rust,python,ts,js,react,nextjs,nodejs,postgres,redis,kafka,docker,kubernetes,grafana,prometheus,aws,gcp,linux,bash&perline=10" />
</p>

### By the numbers

<p>
<img src="https://github-readme-stats.vercel.app/api?username=SAY-5&show_icons=true&count_private=true&hide_border=true&bg_color=07080A&title_color=4AF0C0&icon_color=F0A04A&text_color=E8EAED&ring_color=4AF0C0" height="170" />
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=SAY-5&layout=compact&hide_border=true&bg_color=07080A&title_color=4AF0C0&text_color=E8EAED&langs_count=8&hide=html,css" height="170" />
</p>

<img src="https://github-readme-activity-graph.vercel.app/graph?username=SAY-5&bg_color=07080A&color=4AF0C0&line=0EA5E9&point=F0A04A&area=true&hide_border=true&radius=8" width="100%" />

---

<div align="center">
<sub>Open to building hard systems with thoughtful people. <a href="mailto:saiasish.cnp@gmail.com">Let's talk →</a></sub>
</div>
