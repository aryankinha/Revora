"use client";

import React, { useState, useEffect, useRef } from "react";
import styles from "./Navbar.module.css";

const GridIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="currentColor"
    className={styles.gridIcon}
  >
    <path fillRule="evenodd" d="M3 4.25a1.25 1.25 0 1 1 2.5 0 1.25 1.25 0 0 1-2.5 0ZM3 12a1.25 1.25 0 1 1 2.5 0 1.25 1.25 0 0 1-2.5 0ZM3 19.75a1.25 1.25 0 1 1 2.5 0 1.25 1.25 0 0 1-2.5 0ZM10.75 4.25a1.25 1.25 0 1 1 2.5 0 1.25 1.25 0 0 1-2.5 0ZM10.75 12a1.25 1.25 0 1 1 2.5 0 1.25 1.25 0 0 1-2.5 0ZM10.75 19.75a1.25 1.25 0 1 1 2.5 0 1.25 1.25 0 0 1-2.5 0ZM18.5 4.25a1.25 1.25 0 1 1 2.5 0 1.25 1.25 0 0 1-2.5 0ZM18.5 12a1.25 1.25 0 1 1 2.5 0 1.25 1.25 0 0 1-2.5 0ZM18.5 19.75a1.25 1.25 0 1 1 2.5 0 1.25 1.25 0 0 1-2.5 0Z" clipRule="evenodd" />
  </svg>
);

const CalendarIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    style={{ width: '18px', height: '18px' }}
  >
    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
    <line x1="16" y1="2" x2="16" y2="6"></line>
    <line x1="8" y1="2" x2="8" y2="6"></line>
    <line x1="3" y1="10" x2="21" y2="10"></line>
  </svg>
);

const NAV_LINKS = [
  {
    name: "Product",
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>
    )
  },
  {
     name: "Solutions",
     icon: (
       <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
     )
  },
  {
     name: "Resources",
     icon: (
       <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0 5H20"></path></svg>
     )
  },
  {
     name: "Pricing",
     icon: (
       <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="2" y="5" width="20" height="14" rx="2"></rect><line x1="2" y1="10" x2="22" y2="10"></line></svg>
     )
  }
];

export default function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const checkAuthStatus = () => {
      const token = localStorage.getItem("token");
      setIsAuthenticated(!!token);
    };

    checkAuthStatus();
    
    // Listen for custom auth events to instantly update without a refresh
    window.addEventListener("auth-changed", checkAuthStatus);
    
    return () => window.removeEventListener("auth-changed", checkAuthStatus);
  }, []);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 50) {
        setIsScrolled(true);
        if (isMenuOpen) setIsMenuOpen(false);
      } else {
        setIsScrolled(false);
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, [isMenuOpen]);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (navRef.current && !navRef.current.contains(event.target as Node)) {
        setIsMenuOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleNavClick = (e: React.MouseEvent<HTMLAnchorElement>, name: string) => {
    e.preventDefault();
    const targetId = name.toLowerCase();
    const element = document.getElementById(targetId);
    if (element) {
      // Small offset for the fixed navbar
      const y = element.getBoundingClientRect().top + window.scrollY - 80;
      window.scrollTo({ top: y, behavior: "smooth" });
      setIsMenuOpen(false);
    }
  };

  const openAuthModal = () => {
    window.dispatchEvent(new CustomEvent("open-auth-modal"));
  };

  return (
    <div className={styles.navWrapper} ref={navRef}>
      <nav className={`${styles.navbar} ${isScrolled ? styles.navbarScrolled : ""}`}>
        <div className={styles.navMain}>
          <div className={styles.logo}>
            <span>r</span>evora
          </div>
          
          {/* Inline menu shown when scrolled */}
          <div className={`${styles.inlineMenu} ${isScrolled ? styles.showInline : ""}`}>
            {NAV_LINKS.map(link => (
              <a 
                key={link.name} 
                href={`#${link.name.toLowerCase()}`} 
                onClick={(e) => handleNavClick(e, link.name)}
                className={styles.inlineLink}
              >
                {link.name}
              </a>
            ))}
          </div>

          <div className={styles.icons}>
            {/* Grid Icon hidden when scrolled */}
            <div 
              className={`${styles.gridIconWrapper} ${isScrolled ? styles.hideGrid : ""}`}
              onClick={() => !isScrolled && setIsMenuOpen(!isMenuOpen)}
            >
              <GridIcon />
            </div>
            
            {isAuthenticated ? (
              <a href="/dashboard" className={styles.getStartedBtn} style={{ textDecoration: 'none' }}>
                Dashboard
              </a>
            ) : (
              <button className={styles.getStartedBtn} onClick={openAuthModal}>
                Get started
              </button>
            )}

            <button 
              className={styles.calendarBtn} 
              aria-label="Book Demo"
              onClick={() => window.dispatchEvent(new Event("open-launch-modal"))}
            >
              <CalendarIcon />
            </button>
          </div>
        </div>
      </nav>

      {/* Dropdown Menu - Shown only when at top AND menu is open */}
      <div className={`${styles.dropdownMenu} ${isMenuOpen && !isScrolled ? styles.showDropdown : ""}`}>
        {NAV_LINKS.map(link => (
          <a 
            key={link.name} 
            href={`#${link.name.toLowerCase()}`} 
            onClick={(e) => handleNavClick(e, link.name)}
            className={styles.dropdownLink}
          >
            <span className={styles.dropdownIcon}>{link.icon}</span>
            {link.name}
          </a>
        ))}
      </div>
    </div>
  );
}
