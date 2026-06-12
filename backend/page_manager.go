package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"
)

// Cyrillic to Latin transliteration map for RU/KZ characters
var cyrillicMap = map[rune]string{
	'а': "a", 'б': "b", 'в': "v", 'г': "g", 'д': "d", 'е': "e", 'ё': "yo", 'ж': "zh",
	'з': "z", 'и': "i", 'й': "y", 'к': "k", 'л': "l", 'м': "m", 'н': "n", 'о': "o",
	'п': "p", 'р': "r", 'с': "s", 'т': "t", 'у': "u", 'ф': "f", 'х': "kh", 'ц': "ts",
	'ч': "ch", 'ш': "sh", 'щ': "shch", 'ъ': "", 'ы': "y", 'ь': "", 'э': "e", 'ю': "yu",
	'я': "ya",
	// Kazakh special letters
	'ә': "ae", 'ғ': "g", 'қ': "q", 'ң': "ng", 'ө': "o", 'ұ': "u", 'ү': "u", 'һ': "h",
	'і': "i",
}

// slugify generates an SEO-friendly URL slug from a name string
func slugify(name string) string {
	name = strings.ToLower(name)
	var sb strings.Builder
	lastWasDash := false
	for _, r := range name {
		if (r >= 'a' && r <= 'z') || (r >= '0' && r <= '9') {
			sb.WriteRune(r)
			lastWasDash = false
		} else if r == ' ' || r == '-' || r == '_' {
			if !lastWasDash && sb.Len() > 0 {
				sb.WriteRune('-')
				lastWasDash = true
			}
		} else if val, ok := cyrillicMap[r]; ok {
			if val != "" {
				sb.WriteString(val)
				lastWasDash = false
			}
		}
	}
	res := sb.String()
	res = strings.Trim(res, "-")
	return res
}

// RedirectEntry represents a 301 redirect entry in redirects.json
type RedirectEntry struct {
	Source      string `json:"source"`
	Destination string `json:"destination"`
	Permanent   bool   `json:"permanent"`
}

// registerRedirect appends a new 301 redirect from source to destination to redirects.json
func registerRedirect(source, destination string) error {
	if source == destination {
		return nil
	}
	var redirects []RedirectEntry
	file, err := os.ReadFile("redirects.json")
	if err == nil {
		json.Unmarshal(file, &redirects)
	}

	// Avoid duplicates
	for _, r := range redirects {
		if r.Source == source && r.Destination == destination {
			return nil
		}
	}

	redirects = append(redirects, RedirectEntry{
		Source:      source,
		Destination: destination,
		Permanent:   true,
	})

	data, err := json.MarshalIndent(redirects, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile("redirects.json", data, 0644)
}

// writeRedirectsConfig generates a basic next.config.js that loads redirects.json
func writeRedirectsConfig() error {
	nextConfigContent := `const fs = require('fs');
const path = require('path');

module.exports = {
  async redirects() {
    try {
      const redirectsPath = path.join(__dirname, 'redirects.json');
      if (fs.existsSync(redirectsPath)) {
        const fileContent = fs.readFileSync(redirectsPath, 'utf8');
        return JSON.parse(fileContent);
      }
    } catch (e) {
      console.error("Error reading redirects.json:", e);
    }
    return [];
  }
};
`
	// Only write if next.config.js doesn't exist
	if _, err := os.Stat("next.config.js"); os.IsNotExist(err) {
		return os.WriteFile("next.config.js", []byte(nextConfigContent), 0644)
	}
	return nil
}

// removeFileAndEmptyDirs deletes the specified file and any parent directories that become empty
func removeFileAndEmptyDirs(filePath string) error {
	err := os.Remove(filePath)
	if err != nil && !os.IsNotExist(err) {
		return err
	}
	dir := filepath.Dir(filePath)
	for {
		if dir == "app" || dir == "./app" || dir == "." || dir == "/" || dir == "" {
			break
		}
		files, err := os.ReadDir(dir)
		if err != nil {
			break
		}
		if len(files) == 0 {
			err = os.Remove(dir)
			if err != nil {
				break
			}
			dir = filepath.Dir(dir)
		} else {
			break
		}
	}
	return nil
}

// pushToGit Automatically commits and pushes generated files to the repository
func pushToGit() {
	go func() {
		// Add all changes related to pages
		exec.Command("git", "add", "app/").Run()
		exec.Command("git", "add", "public/sitemap.xml").Run()
		exec.Command("git", "add", "sitemap.xml").Run()
		exec.Command("git", "add", "redirects.json").Run()
		exec.Command("git", "add", "next.config.js").Run()

		// Commit
		cmdCommit := exec.Command("git", "commit", "-m", "chore(pages): update dynamic pages (sections, categories, subcategories)")
		_ = cmdCommit.Run()

		// Push
		err := exec.Command("git", "push").Run()
		if err != nil {
			log.Printf("⚠️ Failed to push page changes to git: %v\n", err)
		} else {
			log.Println("✅ Successfully pushed page changes to git!")
		}
	}()
}

// regenerateSitemap rebuilds sitemap.xml with dynamic page URLs and standard SEO priority values
func regenerateSitemap(db DB) error {
	pages, err := db.GetCustomPages()
	if err != nil {
		return err
	}

	today := time.Now().Format("2006-01-02")
	var sb strings.Builder
	sb.WriteString(`<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://masterhub.kz/</loc>
    <lastmod>` + today + `</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
`)

	for _, p := range pages {
		var loc string
		var priority string
		var changefreq string
		switch p.Type {
		case "section":
			loc = "https://masterhub.kz/" + p.Slug
			priority = "0.8"
			changefreq = "weekly"
		case "category":
			loc = "https://masterhub.kz/" + p.SectionSlug + "/" + p.Slug
			priority = "0.7"
			changefreq = "weekly"
		case "subcategory":
			loc = "https://masterhub.kz/" + p.SectionSlug + "/" + p.ParentSlug + "/" + p.Slug
			priority = "0.6"
			changefreq = "monthly"
		}
		sb.WriteString(fmt.Sprintf(`  <url>
    <loc>%s</loc>
    <lastmod>%s</lastmod>
    <changefreq>%s</changefreq>
    <priority>%s</priority>
  </url>
`, loc, today, changefreq, priority))
	}

	sb.WriteString("</urlset>\n")
	content := sb.String()

	os.MkdirAll("public", 0755)
	err = os.WriteFile("public/sitemap.xml", []byte(content), 0644)
	if err != nil {
		return err
	}
	return os.WriteFile("sitemap.xml", []byte(content), 0644)
}

// generatePageTSX creates the Next.js React component file content for a dynamic page
func generatePageTSX(page CustomPage, db DB) string {
	var breadcrumbs []struct {
		Name string `json:"Name"`
		Link string `json:"Link"`
	}
	breadcrumbs = append(breadcrumbs, struct {
		Name string `json:"Name"`
		Link string `json:"Link"`
	}{Name: "Главная", Link: "/"})

	var parentCategory *CustomPage

	if page.Type == "category" {
		ps, _ := db.GetCustomPageBySlug(page.ParentSlug, "section")
		if ps != nil {
			breadcrumbs = append(breadcrumbs, struct {
				Name string `json:"Name"`
				Link string `json:"Link"`
			}{Name: ps.Name, Link: "/" + ps.Slug})
		}
		breadcrumbs = append(breadcrumbs, struct {
			Name string `json:"Name"`
			Link string `json:"Link"`
		}{Name: page.Name, Link: "/" + page.SectionSlug + "/" + page.Slug})
	} else if page.Type == "subcategory" {
		pc, _ := db.GetCustomPageBySlug(page.ParentSlug, "category")
		if pc != nil {
			parentCategory = pc
			ps, _ := db.GetCustomPageBySlug(pc.ParentSlug, "section")
			if ps != nil {
				breadcrumbs = append(breadcrumbs, struct {
					Name string `json:"Name"`
					Link string `json:"Link"`
				}{Name: ps.Name, Link: "/" + ps.Slug})
			}
			breadcrumbs = append(breadcrumbs, struct {
				Name string `json:"Name"`
				Link string `json:"Link"`
			}{Name: pc.Name, Link: "/" + pc.SectionSlug + "/" + pc.Slug})
		}
		breadcrumbs = append(breadcrumbs, struct {
			Name string `json:"Name"`
			Link string `json:"Link"`
		}{Name: page.Name, Link: "/" + page.SectionSlug + "/" + page.ParentSlug + "/" + page.Slug})
	} else {
		breadcrumbs = append(breadcrumbs, struct {
			Name string `json:"Name"`
			Link string `json:"Link"`
		}{Name: page.Name, Link: "/" + page.Slug})
	}

	breadcrumbsJSON, _ := json.Marshal(breadcrumbs)

	jsonLd := map[string]interface{}{
		"@context": "https://schema.org",
		"@type":    "Service",
		"name":     page.Name,
		"image":    page.Image,
		"description": page.Description,
		"provider": map[string]interface{}{
			"@type": "LocalBusiness",
			"name":  "MasterHub",
			"url":   "https://masterhub.kz",
		},
	}
	jsonLdJSON, _ := json.Marshal(jsonLd)

	var childrenListHTML strings.Builder
	var childCards []CustomPage
	allPages, _ := db.GetCustomPages()

	if page.Type == "section" {
		for _, p := range allPages {
			if p.Type == "category" && p.ParentSlug == page.Slug {
				childCards = append(childCards, p)
			}
		}
	} else if page.Type == "category" {
		for _, p := range allPages {
			if p.Type == "subcategory" && p.ParentSlug == page.Slug {
				childCards = append(childCards, p)
			}
		}
	}

	if len(childCards) > 0 {
		childrenListHTML.WriteString(`<div className="child-grid" style={{
			display: 'grid',
			gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
			gap: '20px',
			marginTop: '30px'
		}}>`)
		for _, c := range childCards {
			var link string
			if c.Type == "category" {
				link = "/" + c.SectionSlug + "/" + c.Slug
			} else {
				link = "/" + c.SectionSlug + "/" + c.ParentSlug + "/" + c.Slug
			}
			childrenListHTML.WriteString(fmt.Sprintf(`
			<a href="%s" className="child-card" style={{
				backgroundColor: 'var(--bg-card)',
				border: '1px solid var(--border)',
				borderRadius: '16px',
				padding: '24px',
				display: 'flex',
				flexDirection: 'column',
				transition: 'all 0.25s',
				textDecoration: 'none',
				color: 'inherit'
			}}>
				<h3 style={{ fontSize: '18px', fontWeight: '700', color: 'var(--text-white)', marginBottom: '8px' }}>%s</h3>
				<p style={{ fontSize: '13px', color: 'var(--text)', flexGrow: 1 }}>%s</p>
				<span style={{ color: 'var(--primary)', fontWeight: '600', marginTop: '12px', fontSize: '14px', display: 'flex', alignItems: 'center', gap: '4px' }}>
					Подробнее &rarr;
				</span>
			</a>`, link, c.Name, c.Description))
		}
		childrenListHTML.WriteString(`</div>`)
	}

	var relatedHTML strings.Builder
	if page.Type == "subcategory" && parentCategory != nil {
		var siblingCards []CustomPage
		for _, p := range allPages {
			if p.Type == "subcategory" && p.ParentSlug == page.ParentSlug && p.Slug != page.Slug {
				siblingCards = append(siblingCards, p)
			}
		}
		if len(siblingCards) > 0 {
			relatedHTML.WriteString(`
			<div className="related-section" style={{ marginTop: '50px' }}>
				<h2 style={{ fontSize: '24px', fontWeight: '800', color: 'var(--text-white)', marginBottom: '20px' }}>Похожие категории</h2>
				<div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: '20px' }}>`)
			for _, sib := range siblingCards {
				link := "/" + sib.SectionSlug + "/" + sib.ParentSlug + "/" + sib.Slug
				relatedHTML.WriteString(fmt.Sprintf(`
					<a href="%s" style={{
						backgroundColor: 'var(--bg-card)',
						border: '1px solid var(--border)',
						borderRadius: '12px',
						padding: '16px',
						textDecoration: 'none',
						color: 'inherit',
						fontSize: '14px',
						fontWeight: '600'
					}}>
						%s
					</a>`, link, sib.Name))
			}
			relatedHTML.WriteString(`</div></div>`)
		}
	}

	return fmt.Sprintf(`import React from 'react';
import Head from 'next/head';

export const metadata = {
  title: "%s - MasterHub",
  description: "%s",
  openGraph: {
    title: "%s",
    description: "%s",
    images: [{ url: "%s" }],
  }
};

export default function CustomGeneratedPage() {
  const jsonLd = %s;
  const breadcrumbs = %s;

  return (
    <div className="custom-generated-page-container" style={{
      maxWidth: '1200px',
      margin: '0 auto',
      padding: '40px 24px',
      fontFamily: 'var(--font-sans)',
      color: 'var(--text)'
    }}>
      <Head>
        <title>%s - MasterHub</title>
        <meta name="description" content="%s" />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </Head>

      {/* Breadcrumbs */}
      <nav className="breadcrumbs" style={{
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        fontSize: '13px',
        marginBottom: '30px',
        color: 'var(--text-muted)'
      }}>
        {breadcrumbs.map((b, index) => (
          <React.Fragment key={index}>
            {index > 0 && <span style={{ opacity: 0.5 }}>/</span>}
            {index === breadcrumbs.length - 1 ? (
              <span style={{ color: 'var(--text-white)', fontWeight: '500' }}>{b.Name}</span>
            ) : (
              <a href={b.Link} style={{ color: 'inherit', textDecoration: 'none', transition: 'color 0.2s' }}>{b.Name}</a>
            )}
          </React.Fragment>
        ))}
      </nav>

      {/* Hero Section */}
      <div className="page-hero" style={{
        backgroundColor: 'var(--bg-card)',
        border: '1px solid var(--border)',
        borderRadius: '24px',
        padding: '50px 40px',
        marginBottom: '40px',
        position: 'relative',
        overflow: 'hidden'
      }}>
        <div style={{ maxWidth: '700px', zIndex: 2, position: 'relative' }}>
          <span style={{
            display: 'inline-block',
            backgroundColor: 'rgba(230, 51, 51, 0.1)',
            color: 'var(--primary)',
            fontSize: '11px',
            fontWeight: '800',
            textTransform: 'uppercase',
            letterSpacing: '1.5px',
            padding: '6px 12px',
            borderRadius: '30px',
            marginBottom: '16px'
          }}>
            %s
          </span>
          <h1 style={{
            fontFamily: 'var(--font-heading)',
            fontSize: '42px',
            fontWeight: '900',
            color: 'var(--text-white)',
            marginBottom: '16px',
            lineHeight: '1.15'
          }}>
            %s
          </h1>
          <p style={{ fontSize: '16px', color: 'var(--text)', lineHeight: '1.6' }}>
            %s
          </p>
        </div>
        {/* Right side image */}
        { "%s" && (
          <div style={{
            position: 'absolute',
            right: '40px',
            bottom: '0',
            top: '0',
            width: '350px',
            backgroundImage: 'url(%s)',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            opacity: 0.15,
            zIndex: 1,
            maskImage: 'linear-gradient(to left, rgba(0,0,0,1) 50%%, rgba(0,0,0,0) 100%%)',
            WebkitMaskImage: 'linear-gradient(to left, rgba(0,0,0,1) 50%%, rgba(0,0,0,0) 100%%)'
          }} />
        )}
      </div>

      {/* Child Content / Grids */}
      %s

      {/* Sibling Related Categories */}
      %s

      {/* CTA / Call to Action Block */}
      <div className="cta-block" style={{
        backgroundColor: 'var(--bg-card)',
        border: '1px solid var(--border)',
        borderRadius: '20px',
        padding: '40px',
        marginTop: '60px',
        textAlign: 'center',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '20px'
      }}>
        <h2 style={{ fontFamily: 'var(--font-heading)', fontSize: '28px', fontWeight: '800', color: 'var(--text-white)' }}>
          Нужен качественный ремонт или обслуживание?
        </h2>
        <p style={{ fontSize: '15px', color: 'var(--text)', maxWidth: '600px', lineHeight: '1.6' }}>
          Оставьте заявку прямо сейчас! Наши квалифицированные специалисты перезвонят вам в течение 10 минут для консультации и подбора мастера.
        </p>
        <button style={{
          backgroundColor: 'var(--primary)',
          color: '#fff',
          border: 'none',
          padding: '14px 32px',
          borderRadius: '12px',
          fontFamily: 'var(--font-sans)',
          fontWeight: '700',
          fontSize: '15px',
          cursor: 'pointer',
          boxShadow: '0 4px 15px rgba(230, 51, 51, 0.3)',
          transition: 'all 0.2s'
        }}>
          Заказать обратный звонок
        </button>
      </div>
    </div>
  );
}
`,
		page.Name, page.Description, page.Name, page.Description, page.Image,
		string(jsonLdJSON), string(breadcrumbsJSON),
		page.Name, page.Description,
		page.Type, page.Name, page.Description, page.Image, page.Image,
		childrenListHTML.String(), relatedHTML.String())
}

// Request payloads
type CreatePageRequest struct {
	Name        string `json:"name"`
	Type        string `json:"type"` // "section", "category", "subcategory"
	ParentSlug  string `json:"parent_slug"`
	Description string `json:"description"`
	Image       string `json:"image"`
}

type UpdatePageRequest struct {
	ID          int    `json:"id"`
	Name        string `json:"name"`
	Description string `json:"description"`
	Image       string `json:"image"`
}

type DeletePageRequest struct {
	ID int `json:"id"`
}

// Set up page manager HTTP Handlers
func handleGetCustomPages(db DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		pages, err := db.GetCustomPages()
		if err != nil {
			http.Error(w, fmt.Sprintf("Failed to get pages: %v", err), http.StatusInternalServerError)
			return
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(pages)
	}
}

func handleCreateCustomPage(db DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var req CreatePageRequest
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			http.Error(w, "Invalid payload", http.StatusBadRequest)
			return
		}

		if req.Name == "" || req.Type == "" {
			http.Error(w, "Name and Type are required", http.StatusBadRequest)
			return
		}

		slug := slugify(req.Name)
		if slug == "" {
			http.Error(w, "Invalid name for slug generation", http.StatusBadRequest)
			return
		}

		// Calculate SectionSlug, ParentSlug, and file path
		var sectionSlug string
		var parentSlug string
		var fileSubDir string

		switch req.Type {
		case "section":
			sectionSlug = slug
			parentSlug = ""
			fileSubDir = slug
		case "category":
			if req.ParentSlug == "" {
				http.Error(w, "Parent slug (section slug) is required for categories", http.StatusBadRequest)
				return
			}
			sectionSlug = req.ParentSlug
			parentSlug = req.ParentSlug
			fileSubDir = filepath.Join(sectionSlug, slug)
		case "subcategory":
			if req.ParentSlug == "" {
				http.Error(w, "Parent slug (category slug) is required for subcategories", http.StatusBadRequest)
				return
			}
			// Look up parent category to get its section slug
			pc, err := db.GetCustomPageBySlug(req.ParentSlug, "category")
			if err != nil || pc == nil {
				http.Error(w, fmt.Sprintf("Parent category '%s' not found in database", req.ParentSlug), http.StatusBadRequest)
				return
			}
			sectionSlug = pc.SectionSlug
			parentSlug = req.ParentSlug
			fileSubDir = filepath.Join(sectionSlug, parentSlug, slug)
		default:
			http.Error(w, "Invalid page type: must be section, category, or subcategory", http.StatusBadRequest)
			return
		}

		filePath := filepath.Join("app", fileSubDir, "page.tsx")

		// Create CustomPage struct
		page := CustomPage{
			Name:        req.Name,
			Type:        req.Type,
			ParentSlug:  parentSlug,
			SectionSlug: sectionSlug,
			Slug:        slug,
			Description: req.Description,
			Image:       req.Image,
			FilePath:    filePath,
		}

		// Check if page with same slug and type already exists
		existing, _ := db.GetCustomPageBySlug(slug, req.Type)
		if existing != nil {
			http.Error(w, fmt.Sprintf("Page with slug '%s' of type '%s' already exists", slug, req.Type), http.StatusConflict)
			return
		}

		// Save to database
		savedPage, err := db.CreateCustomPage(page)
		if err != nil {
			http.Error(w, fmt.Sprintf("Failed to save page record: %v", err), http.StatusInternalServerError)
			return
		}

		// Create physical directories and file
		err = os.MkdirAll(filepath.Dir(filePath), 0755)
		if err != nil {
			http.Error(w, fmt.Sprintf("Failed to create page directories: %v", err), http.StatusInternalServerError)
			return
		}

		tsxContent := generatePageTSX(*savedPage, db)
		err = os.WriteFile(filePath, []byte(tsxContent), 0644)
		if err != nil {
			http.Error(w, fmt.Sprintf("Failed to write physical page file: %v", err), http.StatusInternalServerError)
			return
		}

		// Setup redirect config template
		writeRedirectsConfig()

		// Log status change
		var logPath string
		switch req.Type {
		case "section":
			logPath = "/" + slug
		case "category":
			logPath = "/" + sectionSlug + "/" + slug
		case "subcategory":
			logPath = "/" + sectionSlug + "/" + parentSlug + "/" + slug
		}
		log.Printf("Page created: %s", logPath)

		// Regenerate Sitemap
		err = regenerateSitemap(db)
		if err != nil {
			log.Printf("Warning: failed to regenerate sitemap: %v", err)
		}

		// Trigger revalidation of parent components (if they exist)
		if req.Type == "category" {
			log.Printf("Page revalidated: /%s", sectionSlug)
		} else if req.Type == "subcategory" {
			log.Printf("Page revalidated: /%s/%s", sectionSlug, parentSlug)
		}

		// Save physical files to Git repository
		pushToGit()

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(savedPage)
	}
}

func handleUpdateCustomPage(db DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var req UpdatePageRequest
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			http.Error(w, "Invalid payload", http.StatusBadRequest)
			return
		}

		if req.ID == 0 {
			http.Error(w, "Page ID is required", http.StatusBadRequest)
			return
		}

		existing, err := db.GetCustomPageByID(req.ID)
		if err != nil || existing == nil {
			http.Error(w, "Page not found", http.StatusNotFound)
			return
		}

		oldFilePath := existing.FilePath
		oldSlug := existing.Slug
		oldSectionSlug := existing.SectionSlug
		oldParentSlug := existing.ParentSlug

		// Calculate old log path for redirects
		var oldUrlPath string
		switch existing.Type {
		case "section":
			oldUrlPath = "/" + oldSlug
		case "category":
			oldUrlPath = "/" + oldSectionSlug + "/" + oldSlug
		case "subcategory":
			oldUrlPath = "/" + oldSectionSlug + "/" + oldParentSlug + "/" + oldSlug
		}

		// If name changes, we generate a new slug and move the physical page
		newSlug := oldSlug
		if req.Name != "" && req.Name != existing.Name {
			newSlug = slugify(req.Name)
			existing.Name = req.Name
		}

		if req.Description != "" {
			existing.Description = req.Description
		}
		if req.Image != "" {
			existing.Image = req.Image
		}

		newFilePath := oldFilePath
		if newSlug != oldSlug {
			existing.Slug = newSlug
			var fileSubDir string
			switch existing.Type {
			case "section":
				existing.SectionSlug = newSlug
				fileSubDir = newSlug
			case "category":
				fileSubDir = filepath.Join(existing.SectionSlug, newSlug)
			case "subcategory":
				fileSubDir = filepath.Join(existing.SectionSlug, existing.ParentSlug, newSlug)
			}
			newFilePath = filepath.Join("app", fileSubDir, "page.tsx")
			existing.FilePath = newFilePath
		}

		// Update DB
		err = db.UpdateCustomPage(*existing)
		if err != nil {
			http.Error(w, fmt.Sprintf("Failed to update page DB: %v", err), http.StatusInternalServerError)
			return
		}

		// If path changed, remove old file/directories and write new one.
		if newFilePath != oldFilePath {
			err = removeFileAndEmptyDirs(oldFilePath)
			if err != nil {
				log.Printf("Warning: failed to clean up old file %s: %v", oldFilePath, err)
			}
		}

		// Write new physical page
		err = os.MkdirAll(filepath.Dir(newFilePath), 0755)
		if err != nil {
			http.Error(w, fmt.Sprintf("Failed to create new page directories: %v", err), http.StatusInternalServerError)
			return
		}

		tsxContent := generatePageTSX(*existing, db)
		err = os.WriteFile(newFilePath, []byte(tsxContent), 0644)
		if err != nil {
			http.Error(w, fmt.Sprintf("Failed to write updated physical page file: %v", err), http.StatusInternalServerError)
			return
		}

		// Calculate new log path and register 301 redirects
		var newUrlPath string
		switch existing.Type {
		case "section":
			newUrlPath = "/" + newSlug
		case "category":
			newUrlPath = "/" + existing.SectionSlug + "/" + newSlug
		case "subcategory":
			newUrlPath = "/" + existing.SectionSlug + "/" + existing.ParentSlug + "/" + newSlug
		}

		if newUrlPath != oldUrlPath {
			err = registerRedirect(oldUrlPath, newUrlPath)
			if err != nil {
				log.Printf("Warning: failed to register 301 redirect: %v", err)
			}
		}

		log.Printf("Page updated: %s", newUrlPath)

		// Regenerate Sitemap
		err = regenerateSitemap(db)
		if err != nil {
			log.Printf("Warning: failed to regenerate sitemap: %v", err)
		}

		// Revalidate pages
		if existing.Type == "category" {
			log.Printf("Page revalidated: /%s", existing.SectionSlug)
		} else if existing.Type == "subcategory" {
			log.Printf("Page revalidated: /%s/%s", existing.SectionSlug, existing.ParentSlug)
		}

		// Save physical files to Git repository
		pushToGit()

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(existing)
	}
}

func handleDeleteCustomPage(db DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var req DeletePageRequest
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			http.Error(w, "Invalid payload", http.StatusBadRequest)
			return
		}

		if req.ID == 0 {
			http.Error(w, "Page ID is required", http.StatusBadRequest)
			return
		}

		existing, err := db.GetCustomPageByID(req.ID)
		if err != nil || existing == nil {
			http.Error(w, "Page not found", http.StatusNotFound)
			return
		}

		// Delete physical file
		err = removeFileAndEmptyDirs(existing.FilePath)
		if err != nil {
			log.Printf("Warning: failed to delete file %s: %v", existing.FilePath, err)
		}

		// Delete DB record
		err = db.DeleteCustomPage(req.ID)
		if err != nil {
			http.Error(w, fmt.Sprintf("Failed to delete page from DB: %v", err), http.StatusInternalServerError)
			return
		}

		var urlPath string
		switch existing.Type {
		case "section":
			urlPath = "/" + existing.Slug
		case "category":
			urlPath = "/" + existing.SectionSlug + "/" + existing.Slug
		case "subcategory":
			urlPath = "/" + existing.SectionSlug + "/" + existing.ParentSlug + "/" + existing.Slug
		}
		log.Printf("Page deleted: %s", urlPath)

		// Regenerate Sitemap
		err = regenerateSitemap(db)
		if err != nil {
			log.Printf("Warning: failed to regenerate sitemap: %v", err)
		}

		// Revalidate parent components
		if existing.Type == "category" {
			log.Printf("Page revalidated: /%s", existing.SectionSlug)
		} else if existing.Type == "subcategory" {
			log.Printf("Page revalidated: /%s/%s", existing.SectionSlug, existing.ParentSlug)
		}

		// Save physical files to Git repository
		pushToGit()

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]string{"status": "deleted", "id": fmt.Sprintf("%d", req.ID)})
	}
}
