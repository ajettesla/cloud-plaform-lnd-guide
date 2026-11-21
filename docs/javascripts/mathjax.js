// MathJax configuration for KaTeX-style math rendering
window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    processEscapes: true,
    processEnvironments: true,
    tags: 'ams',
    macros: {
      // Common LND/Cloud macros
      LND: '{\\text{LND}}',
      BTC: '{\\text{BTC}}',
      sat: '{\\text{sat}}',
      HTLC: '{\\text{HTLC}}',
      IOPS: '{\\text{IOPS}}',
      CPU: '{\\text{CPU}}',
      RAM: '{\\text{RAM}}',
      GB: '{\\text{GB}}',
      TB: '{\\text{TB}}',
      USD: '{\\text{USD}}',
      AWS: '{\\text{AWS}}',
      GCP: '{\\text{GCP}}',
      Azure: '{\\text{Azure}}',
    }
  },
  options: {
    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'],
    ignoreHtmlClass: 'tex2jax_ignore',
    processHtmlClass: 'tex2jax_process'
  },
  startup: {
    ready: () => {
      MathJax.startup.defaultReady();
      // Re-process after MkDocs navigation
      document.addEventListener('DOMContentLoaded', () => {
        MathJax.typesetPromise();
      });
    }
  }
};
