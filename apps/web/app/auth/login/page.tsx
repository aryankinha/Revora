"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import styles from "../auth.module.css";
import Navbar from "../../../components/landing/Navbar";

export default function LoginPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const email = form.get("email") as string;
    const password = form.get("password") as string;
    
    if (!email || !password) {
      setError("Please fill all required fields");
      return;
    }
    
    setLoading(true);
    setError("");

    try {
      const response = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Invalid credentials");
      }

      if (data.access_token) {
         localStorage.setItem("token", data.access_token);
         window.dispatchEvent(new Event("auth-changed"));
      }

      router.push(data.redirect_url || "/dashboard");
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An unknown error occurred");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar />
      <div className={styles.loginPage}>
        <div className={styles.cardWrapper}>
          <div className={styles.card}>
            <h1 className={styles.title}>Revora Agent Login</h1>
            <p className={styles.subtitle}>Hey, Enter your details to get sign in<br/>to your workspace account</p>

            {error && <div style={{ color: "#f05a28", marginBottom: "1rem", fontSize: "0.9rem" }}>{error}</div>}

            <form className={styles.form} onSubmit={handleSubmit}>
              <div className={styles.inputWrapper}>
                <input className={styles.input} name="email" type="email" placeholder="Enter Email / Phone No" required />
                <svg className={styles.inputIcon} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
              </div>
              <div className={styles.inputWrapper}>
                <input className={styles.input} name="password" type="password" placeholder="Passcode" required />
                <svg className={styles.inputIcon} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle><line x1="1" y1="1" x2="23" y2="23"></line></svg>
              </div>

              <Link href="#" className={styles.troubleLink}>Having trouble in sign in?</Link>
              
              <button className={styles.primaryBtn} type="submit" disabled={loading}>
                {loading ? "Signing in..." : "Sign in"}
              </button>
            </form>

            <div className={styles.divider}>Or Sign in with</div>

            <div className={styles.socialGrid}>
              <button className={styles.socialBtn} type="button">
                <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.187 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"/></svg>
                Google
              </button>
              <button className={styles.socialBtn} type="button">
                <svg viewBox="0 0 24 24" fill="currentColor"><path d="M13.435 9.1c0 2.228-1.742 4.093-3.951 4.194-2.274.1-3.99-1.921-3.95-4.148.04-2.28 1.8-4.116 3.99-4.195 2.203-.08 3.91 1.815 3.91 4.149zm-3.824 4.314c-2.37.118-4.43-1.29-5.462-1.29-1.074 0-2.887 1.258-4.755 1.218-2.454-.041-4.71-1.436-5.968-3.64-2.55-4.437-.65-11.01 1.83-14.616 1.22-1.776 2.89-2.924 4.8-2.964 1.83-.042 3.565 1.257 4.7 1.257 1.136 0 3.097-1.517 5.341-1.258 1.438.08 2.502.502 3.652 1.4.385.3 3.614 3.067 3.57 7.734-4.08.384-5.875 4.322-5.717 7.155z"/></svg>
                Apple ID
              </button>
              <button className={styles.socialBtn} type="button">
                <svg viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                Facebook
              </button>
            </div>

            <div className={styles.helper}>
              <span className={styles.helperText}>Don&apos;t have an account?</span>
              <Link href="/auth/signup" className={styles.secondaryBtn}>Request Now</Link>
            </div>

          </div>
        </div>
        <div className={styles.copyright}>Copyright @Revora 2024 | Privacy Policy</div>
      </div>
    </>
  );
}
