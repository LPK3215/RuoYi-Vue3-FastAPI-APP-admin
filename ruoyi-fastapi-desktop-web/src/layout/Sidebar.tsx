import clsx from 'clsx'
import { NavLink } from 'react-router-dom'

function SideItem(props: { to: string; label: string; hint?: string }) {
  return (
    <NavLink
      to={props.to}
      className={({ isActive }) => clsx('ds-sideItem', isActive && 'ds-sideItem--active')}
      end={props.to === '/admin/dashboard'}
    >
      <span className="ds-sideItemLabel">{props.label}</span>
      {props.hint ? <span className="ds-sideItemHint">{props.hint}</span> : null}
    </NavLink>
  )
}

export function Sidebar() {
  return (
    <aside className="ds-sidebar">
      <div className="ds-brand">
        <div className="ds-brandMark" aria-hidden="true">
          <span />
        </div>
        <div className="ds-brandText">
          <div className="ds-brandTitle">{import.meta.env.VITE_APP_TITLE || 'DeskOps'}</div>
          <div className="ds-brandSub">Desktop Web · FastAPI</div>
        </div>
      </div>

      <nav className="ds-nav">
        <div className="ds-navGroup">
          <div className="ds-navGroupTitle">概览</div>
          <SideItem to="/admin/dashboard" label="仪表盘" hint="dashboard" />
        </div>
        <div className="ds-navGroup">
          <div className="ds-navGroupTitle">系统</div>
          <SideItem to="/admin/system/users" label="用户列表" hint="table render" />
        </div>
      </nav>

      <div className="ds-sideFooter">
        <div className="ds-sideFooterLine">
          API: <span className="ds-mono">{import.meta.env.VITE_API_BASE || '/dev-api'}</span>
        </div>
      </div>
    </aside>
  )
}
