import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import { motion } from 'framer-motion';

import styles from './index.module.css';

// Feature Data
const features = [
  {
    title: 'Hybrid Driver Architecture',
    img: require('@site/static/img/feat_hybrid.png').default,
    description: "Empower your testing with true hybrid capability. Execute seamlessly on Selenium for legacy stability or Playwright for modern speed—all from a single, unified API.",
  },
  {
    title: 'Unified API Connectivity',
    img: require('@site/static/img/feat_api.png').default,
    description: "Bridge the gap between UI and Backend. Our unified client handles REST and GraphQL with automatic request logging, error handling, and type-safe responses.",
  },
  {
    title: 'Enterprise Scalability',
    img: require('@site/static/img/feat_scale.png').default,
    description: "Built for the Fortune 500. Includes integrated Database management, detailed Allure reporting, zero-config CI/CD readiness, and robust security practices.",
  },
];

function Hero() {
  const {siteConfig} = useDocusaurusContext();
  
  return (
    <header className="hero-container">
      <motion.div 
        className="hero-content"
        initial={{ opacity: 0, x: -50 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.8 }}
      >
        <Heading as="h1" className="hero-title">
          Next-Gen <br/> QA Automation
        </Heading>
        <p className="hero-subtitle">
          The <strong>QA Framework</strong> is an enterprise-grade core library designed to unify your testing ecosystem. 
          Deliver flawless software faster with our hybrid architecture.
        </p>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', justifyContent: 'center' }}>
             <Link
            className="button button--primary button--lg shadow--md"
            to="/docs/intro">
            Get Started
            </Link>
            <Link
            className="button button--secondary button--lg shadow--md"
            to="/docs/architecture">
            View Architecture
            </Link>
        </div>
      </motion.div>

      <motion.div 
        className="hero-image"
        initial={{ opacity: 0, x: 50, scale: 0.9 }}
        animate={{ opacity: 1, x: 0, scale: 1 }}
        transition={{ duration: 0.8, delay: 0.2 }}
      >
        <img 
            src={require('@site/static/img/hero_3d.png').default} 
            alt="Futuristic Testing Lab"
            style={{ maxWidth: '100%', height: 'auto', filter: 'drop-shadow(0 20px 30px rgba(0,0,0,0.15))' }}
        />
      </motion.div>
    </header>
  );
}

function Features() {
  return (
    <section className="features-section">
      <div className="container">
        <div className="row">
          {features.map((props, idx) => (
            <div key={idx} className="col col--4 margin-bottom--lg">
                <motion.div 
                    className="glass-panel feature-card"
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.5, delay: idx * 0.2 }}
                >
                    <img src={props.img} alt={props.title} className="feature-img" />
                    <Heading as="h3" className="feature-title">{props.title}</Heading>
                    <p className="feature-desc">{props.description}</p>
                </motion.div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title="Enterprise QA Automation"
      description="Next-Generation QA Framework Core Library">
      <main>
        <Hero />
        <Features />
      </main>
    </Layout>
  );
}
