// ANDD wordmark — mark = 3-dot inverted triangle ("upside-down A").
// Two dots at top, one dot at bottom-center. Cyan glow.
window.renderWordmark = function (el, {size = 22, label = true} = {}) {
  el.innerHTML = `
    <span class="wm-mark" style="width:${size}px;height:${size*0.92}px;display:inline-block;position:relative">
      <svg viewBox="0 0 24 22" style="width:100%;height:100%;overflow:visible" aria-hidden="true">
        <defs>
          <filter id="wmGlow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="1.2" result="b"/>
            <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
          </filter>
        </defs>
        <g fill="#5ee3ff" filter="url(#wmGlow)">
          <circle cx="4"  cy="4"  r="2.6"/>
          <circle cx="20" cy="4"  r="2.6"/>
          <circle cx="12" cy="18" r="2.6"/>
        </g>
      </svg>
    </span>
    ${label ? `<span class="wm-text"><span style="font-weight:500">∀</span><span>NDD</span><span class="wm-kern" style="margin-left:8px;font-size:0.7em;align-self:center">/ edge network</span></span>` : ''}
  `;
};
