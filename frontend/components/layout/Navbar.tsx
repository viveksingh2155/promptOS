'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { usePathname, useRouter } from 'next/navigation';
import { useStore } from '@/store/useStore';
import { Zap, Moon, Sun, LogOut, Menu, X } from 'lucide-react';

const NAV_LINKS = [
  { href: '/',           label: 'Workspace' },
  { href: '/history',   label: 'History'   },
  { href: '/templates', label: 'Templates' },
  { href: '/settings',  label: 'Settings'  },
];

export default function Navbar() {
  const pathname = usePathname();
  const router = useRouter();
  const { user, logout, theme, toggleTheme, devMode } = useStore();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const initial = user?.displayName?.charAt(0).toUpperCase() ?? 'J';

  const closeMobileMenu = () => setMobileMenuOpen(false);

  return (
    <>
      <nav className="apple-nav">
        <div style={{
          maxWidth: 1200, margin: '0 auto', width: '100%',
          display: 'flex', alignItems: 'center', justifyContent: 'space-between',
          padding: '0 16px',
        }}>
          {/* Logo */}
          <motion.button
            whileHover={{ scale: 1.06 }}
            whileTap={{ scale: 0.94 }}
            onClick={() => { router.push('/'); closeMobileMenu(); }}
            style={{
              display: 'flex', alignItems: 'center', gap: 12,
              background: 'none', border: 'none', cursor: 'pointer',
              padding: 0,
            }}
          >
            <img
              src="/logo.png"
              alt="PromptOS Logo"
              style={{
                width: 34, height: 34, borderRadius: 8,
                border: '1px solid rgba(41,151,255,0.4)',
                boxShadow: '0 0 14px rgba(41,151,255,0.35)',
                objectFit: 'cover'
              }}
            />
            <span style={{ fontSize: 18, fontWeight: 700, letterSpacing: '-0.02em', color: '#f5f5f7' }} className="hide-mobile">
              PromptOS
            </span>
          </motion.button>

          {/* Desktop nav links */}
          <div className="hide-mobile" style={{ display: 'flex', alignItems: 'center', gap: 28 }}>
            {NAV_LINKS.map(({ href, label }) => {
              const active = pathname === href;
              return (
                <motion.button
                  key={href}
                  onClick={() => router.push(href)}
                  whileTap={{ scale: 0.95 }}
                  className={`nav-link ${active ? 'active' : ''}`}
                  style={{
                    background: 'none', border: 'none', cursor: 'pointer',
                    padding: '14px 0', display: 'block',
                    fontFamily: 'inherit',
                  }}
                >
                  {label}
                </motion.button>
              );
            })}
          </div>

          {/* Right controls */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            {/* Dev badge */}
            <AnimatePresence>
              {devMode && (
                <motion.span
                  initial={{ opacity: 0, scale: 0.8, x: 10 }}
                  animate={{ opacity: 1, scale: 1, x: 0 }}
                  exit={{ opacity: 0, scale: 0.8, x: 10 }}
                  className="dev-badge hide-mobile"
                  style={{ fontSize: 10 }}
                >
                  <span style={{ width: 5, height: 5, borderRadius: '50%', background: '#2997ff', display: 'inline-block' }} />
                  DEV
                </motion.span>
              )}
            </AnimatePresence>

            {/* Theme toggle */}
            <motion.button
              whileHover={{ scale: 1.1, background: 'rgba(255,255,255,0.1)' }}
              whileTap={{ scale: 0.9 }}
              onClick={toggleTheme}
              className="hide-mobile"
              style={{
                width: 34, height: 34, borderRadius: '50%', border: 'none',
                background: 'rgba(255,255,255,0.07)', cursor: 'pointer',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                color: 'rgba(245,245,247,0.7)', transition: 'background 0.15s',
              }}
            >
              <AnimatePresence mode="wait">
                <motion.div
                  key={theme}
                  initial={{ rotate: -30, opacity: 0 }}
                  animate={{ rotate: 0, opacity: 1 }}
                  exit={{ rotate: 30, opacity: 0 }}
                  transition={{ duration: 0.18 }}
                >
                  {theme === 'dark' ? <Moon size={15} /> : <Sun size={15} />}
                </motion.div>
              </AnimatePresence>
            </motion.button>

            {/* User pill + logout - Desktop */}
            {user && (
              <div className="hide-mobile" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                {user.avatar ? (
                  <motion.img
                    whileHover={{ scale: 1.06 }}
                    src={user.avatar}
                    alt={user.displayName}
                    style={{ width: 28, height: 28, borderRadius: '50%', objectFit: 'cover', border: '1.5px solid rgba(255,255,255,0.15)' }}
                  />
                ) : (
                  <motion.div
                    whileHover={{ scale: 1.06 }}
                    style={{
                      width: 28, height: 28, borderRadius: '50%',
                      background: '#0071e3',
                      display: 'flex', alignItems: 'center', justifyContent: 'center',
                      fontSize: 12, fontWeight: 700, color: '#fff',
                      border: '1.5px solid rgba(255,255,255,0.15)',
                    }}
                  >
                    {initial}
                  </motion.div>
                )}
                <span style={{ fontSize: 13, color: 'rgba(245,245,247,0.75)', letterSpacing: '-0.01em' }}>
                  {user.displayName?.split(' ')[0]}
                </span>
                <motion.button
                  whileHover={{ scale: 1.1, color: '#ff453a' }}
                  whileTap={{ scale: 0.9 }}
                  onClick={logout}
                  style={{
                    background: 'none', border: 'none', cursor: 'pointer',
                    color: 'rgba(245,245,247,0.35)', display: 'flex', alignItems: 'center',
                    padding: 4, transition: 'color 0.15s',
                  }}
                  title="Sign out"
                >
                  <LogOut size={14} />
                </motion.button>
              </div>
            )}

            {/* Mobile menu button */}
            <motion.button
              whileTap={{ scale: 0.9 }}
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="hide-desktop"
              style={{
                width: 40, height: 40, borderRadius: '8px', border: 'none',
                background: 'rgba(255,255,255,0.07)', cursor: 'pointer',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                color: 'rgba(245,245,247,0.9)',
              }}
              aria-label="Toggle menu"
            >
              {mobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
            </motion.button>
          </div>
        </div>
      </nav>

      {/* Mobile Menu */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <>
            {/* Overlay */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              onClick={closeMobileMenu}
              className="mobile-menu-overlay"
            />
            
            {/* Drawer */}
            <motion.div
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              transition={{ type: 'spring', damping: 30, stiffness: 300 }}
              className="mobile-drawer"
              style={{
                position: 'fixed',
                top: 56,
                right: 0,
                bottom: 0,
                left: 'auto',
                width: 280,
                maxWidth: '85vw',
              }}
            >
              <div style={{ padding: '24px 20px', display: 'flex', flexDirection: 'column', gap: 20 }}>
                {/* User info */}
                {user && (
                  <div style={{ 
                    display: 'flex', alignItems: 'center', gap: 12,
                    paddingBottom: 20,
                    borderBottom: '1px solid rgba(255,255,255,0.1)'
                  }}>
                    {user.avatar ? (
                      <img
                        src={user.avatar}
                        alt={user.displayName}
                        style={{ width: 40, height: 40, borderRadius: '50%', objectFit: 'cover' }}
                      />
                    ) : (
                      <div style={{
                        width: 40, height: 40, borderRadius: '50%',
                        background: '#0071e3',
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                        fontSize: 16, fontWeight: 700, color: '#fff',
                      }}>
                        {initial}
                      </div>
                    )}
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ fontSize: 15, fontWeight: 600, color: '#f5f5f7', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {user.displayName}
                      </div>
                      {user.email && (
                        <div style={{ fontSize: 13, color: 'rgba(245,245,247,0.5)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                          {user.email}
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Nav links */}
                <nav style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                  {NAV_LINKS.map(({ href, label }) => {
                    const active = pathname === href;
                    return (
                      <motion.button
                        key={href}
                        onClick={() => { router.push(href); closeMobileMenu(); }}
                        whileTap={{ scale: 0.97 }}
                        style={{
                          padding: '14px 16px',
                          background: active ? 'rgba(41,151,255,0.14)' : 'transparent',
                          border: 'none',
                          borderRadius: 10,
                          color: active ? '#2997ff' : 'rgba(245,245,247,0.75)',
                          fontSize: 16,
                          fontWeight: active ? 600 : 400,
                          textAlign: 'left',
                          cursor: 'pointer',
                          fontFamily: 'inherit',
                          transition: 'all 0.15s',
                        }}
                      >
                        {label}
                      </motion.button>
                    );
                  })}
                </nav>

                {/* Theme toggle mobile */}
                <motion.button
                  whileTap={{ scale: 0.97 }}
                  onClick={() => { toggleTheme(); }}
                  style={{
                    padding: '14px 16px',
                    background: 'rgba(255,255,255,0.07)',
                    border: 'none',
                    borderRadius: 10,
                    color: 'rgba(245,245,247,0.75)',
                    fontSize: 16,
                    textAlign: 'left',
                    cursor: 'pointer',
                    fontFamily: 'inherit',
                    display: 'flex',
                    alignItems: 'center',
                    gap: 10,
                  }}
                >
                  {theme === 'dark' ? <Moon size={18} /> : <Sun size={18} />}
                  <span>Switch to {theme === 'dark' ? 'Light' : 'Dark'} Mode</span>
                </motion.button>

                {/* Dev mode badge */}
                {devMode && (
                  <div style={{
                    padding: '12px 16px',
                    background: 'rgba(41,151,255,0.14)',
                    borderRadius: 10,
                    display: 'flex',
                    alignItems: 'center',
                    gap: 8,
                  }}>
                    <span style={{ width: 8, height: 8, borderRadius: '50%', background: '#2997ff' }} />
                    <span style={{ fontSize: 12, fontWeight: 600, color: '#2997ff', letterSpacing: '0.04em', textTransform: 'uppercase' }}>
                      Dev Mode Active
                    </span>
                  </div>
                )}

                {/* Logout button */}
                {user && (
                  <motion.button
                    whileTap={{ scale: 0.97 }}
                    onClick={() => { logout(); closeMobileMenu(); }}
                    style={{
                      padding: '14px 16px',
                      background: 'rgba(255,69,58,0.1)',
                      border: '1px solid rgba(255,69,58,0.3)',
                      borderRadius: 10,
                      color: '#ff453a',
                      fontSize: 16,
                      fontWeight: 500,
                      cursor: 'pointer',
                      fontFamily: 'inherit',
                      display: 'flex',
                      alignItems: 'center',
                      gap: 10,
                      marginTop: 'auto',
                    }}
                  >
                    <LogOut size={18} />
                    <span>Sign Out</span>
                  </motion.button>
                )}
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}
