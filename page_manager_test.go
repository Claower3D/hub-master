package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"testing"
)

func TestPageGenerationFlow(t *testing.T) {
	t.Log("🧪 Starting Page Generation Unit Tests...")

	// 1. Initialize JsonDB
	dbFile := "test_masterhub_data.json"
	os.Remove(dbFile) // start clean
	defer os.Remove(dbFile)

	db, err := NewJsonDB(dbFile)
	if err != nil {
		t.Fatalf("Failed to create test JSON DB: %v", err)
	}

	// Clean up app directory and redirects.json
	os.RemoveAll("app")
	os.Remove("redirects.json")
	defer os.RemoveAll("app")
	defer os.Remove("redirects.json")

	t.Log("Step 1: DB & app directory cleared successfully.")

	// 2. Create Section: "Электроника"
	secSlug := slugify("Электроника")
	if secSlug != "elektronika" {
		t.Errorf("Expected slug 'elektronika', got '%s'", secSlug)
	}

	secPage := CustomPage{
		Name:        "Электроника",
		Type:        "section",
		ParentSlug:  "",
		SectionSlug: secSlug,
		Slug:        secSlug,
		Description: "Раздел электроники",
		Image:       "electronics.png",
		FilePath:    filepath.Join("app", secSlug, "page.tsx"),
	}
	savedSec, err := db.CreateCustomPage(secPage)
	if err != nil {
		t.Fatalf("Failed to create section page: %v", err)
	}
	err = os.MkdirAll(filepath.Dir(savedSec.FilePath), 0755)
	if err != nil {
		t.Fatalf("Mkdir section failed: %v", err)
	}
	err = os.WriteFile(savedSec.FilePath, []byte(generatePageTSX(*savedSec, db)), 0644)
	if err != nil {
		t.Fatalf("Write section file failed: %v", err)
	}
	t.Logf("Created section: %s -> %s", savedSec.Name, savedSec.FilePath)

	// 3. Create Category: "Ремонт" under "Электроника"
	catSlug := slugify("Ремонт")
	if catSlug != "remont" {
		t.Errorf("Expected slug 'remont', got '%s'", catSlug)
	}

	catPage := CustomPage{
		Name:        "Ремонт",
		Type:        "category",
		ParentSlug:  secSlug,
		SectionSlug: secSlug,
		Slug:        catSlug,
		Description: "Категория ремонта",
		Image:       "repair.png",
		FilePath:    filepath.Join("app", secSlug, catSlug, "page.tsx"),
	}
	savedCat, err := db.CreateCustomPage(catPage)
	if err != nil {
		t.Fatalf("Failed to create category page: %v", err)
	}
	err = os.MkdirAll(filepath.Dir(savedCat.FilePath), 0755)
	if err != nil {
		t.Fatalf("Mkdir category failed: %v", err)
	}
	err = os.WriteFile(savedCat.FilePath, []byte(generatePageTSX(*savedCat, db)), 0644)
	if err != nil {
		t.Fatalf("Write category file failed: %v", err)
	}
	t.Logf("Created category: %s -> %s", savedCat.Name, savedCat.FilePath)

	// 4. Create Subcategory: "Ремонт телефонов" under "Ремонт"
	subSlug := slugify("Ремонт телефонов")
	if subSlug != "remont-telefonov" {
		t.Errorf("Expected slug 'remont-telefonov', got '%s'", subSlug)
	}

	subPage := CustomPage{
		Name:        "Ремонт телефонов",
		Type:        "subcategory",
		ParentSlug:  catSlug,
		SectionSlug: secSlug,
		Slug:        subSlug,
		Description: "Ремонт мобильных телефонов любых брендов",
		Image:       "phones.png",
		FilePath:    filepath.Join("app", secSlug, catSlug, subSlug, "page.tsx"),
	}
	savedSub, err := db.CreateCustomPage(subPage)
	if err != nil {
		t.Fatalf("Failed to create subcategory page: %v", err)
	}
	err = os.MkdirAll(filepath.Dir(savedSub.FilePath), 0755)
	if err != nil {
		t.Fatalf("Mkdir subcategory failed: %v", err)
	}
	err = os.WriteFile(savedSub.FilePath, []byte(generatePageTSX(*savedSub, db)), 0644)
	if err != nil {
		t.Fatalf("Write subcategory file failed: %v", err)
	}
	t.Logf("Created subcategory: %s -> %s", savedSub.Name, savedSub.FilePath)

	// Verify all TSX files exist
	if _, err := os.Stat(savedSec.FilePath); err != nil {
		t.Fatalf("Section file does not exist: %v", err)
	}
	if _, err := os.Stat(savedCat.FilePath); err != nil {
		t.Fatalf("Category file does not exist: %v", err)
	}
	if _, err := os.Stat(savedSub.FilePath); err != nil {
		t.Fatalf("Subcategory file does not exist: %v", err)
	}
	t.Log("Verification: All TSX files physically exist on disk.")

	// Verify sitemap.xml
	err = regenerateSitemap(db)
	if err != nil {
		t.Fatalf("Failed to generate sitemap: %v", err)
	}
	if _, err := os.Stat("public/sitemap.xml"); err != nil {
		t.Fatalf("public/sitemap.xml does not exist: %v", err)
	}
	t.Log("Verification: sitemap.xml generated successfully.")

	// 5. Update Subcategory Name: "Ремонт телефонов" -> "Ремонт мобильных телефонов"
	oldFilePath := savedSub.FilePath
	newSlug := slugify("Ремонт мобильных телефонов")
	savedSub.Name = "Ремонт мобильных телефонов"
	savedSub.Slug = newSlug
	savedSub.FilePath = filepath.Join("app", secSlug, catSlug, newSlug, "page.tsx")

	err = db.UpdateCustomPage(*savedSub)
	if err != nil {
		t.Fatalf("Failed to update page in DB: %v", err)
	}

	// Clean up old file
	err = removeFileAndEmptyDirs(oldFilePath)
	if err != nil {
		t.Fatalf("Remove old subcategory file failed: %v", err)
	}

	// Write new file
	err = os.MkdirAll(filepath.Dir(savedSub.FilePath), 0755)
	if err != nil {
		t.Fatalf("Mkdir updated subcategory failed: %v", err)
	}
	err = os.WriteFile(savedSub.FilePath, []byte(generatePageTSX(*savedSub, db)), 0644)
	if err != nil {
		t.Fatalf("Write updated subcategory file failed: %v", err)
	}

	// Register 301 redirect
	oldUrlPath := fmt.Sprintf("/%s/%s/%s", secSlug, catSlug, subSlug)
	newUrlPath := fmt.Sprintf("/%s/%s/%s", secSlug, catSlug, newSlug)
	err = registerRedirect(oldUrlPath, newUrlPath)
	if err != nil {
		t.Fatalf("Failed to register redirect: %v", err)
	}

	t.Logf("Updated subcategory: %s -> %s", savedSub.Name, savedSub.FilePath)

	// Verify old file is gone and new file exists
	if _, err := os.Stat(oldFilePath); !os.IsNotExist(err) {
		t.Fatalf("Old file still exists at %s", oldFilePath)
	}
	if _, err := os.Stat(savedSub.FilePath); err != nil {
		t.Fatalf("New file does not exist at %s", savedSub.FilePath)
	}
	t.Log("Verification: Old file deleted, new file created.")

	// Verify redirects.json
	redirectsFile, err := os.ReadFile("redirects.json")
	if err != nil {
		t.Fatalf("Failed to read redirects.json: %v", err)
	}
	var redirects []RedirectEntry
	json.Unmarshal(redirectsFile, &redirects)
	if len(redirects) != 1 || redirects[0].Source != oldUrlPath || redirects[0].Destination != newUrlPath {
		t.Fatalf("Invalid redirects.json content: %s", string(redirectsFile))
	}
	t.Log("Verification: redirects.json matches expected 301 entry.")

	// 6. Delete Subcategory Page
	err = removeFileAndEmptyDirs(savedSub.FilePath)
	if err != nil {
		t.Fatalf("Delete subcategory file failed: %v", err)
	}
	err = db.DeleteCustomPage(savedSub.ID)
	if err != nil {
		t.Fatalf("Delete subcategory DB record failed: %v", err)
	}

	// Verify file is gone and directories cleaned up
	if _, err := os.Stat(savedSub.FilePath); !os.IsNotExist(err) {
		t.Fatalf("Subcategory page was not deleted physically: %s", savedSub.FilePath)
	}
	// The parent directory of the subcategory was: app/elektronika/remont/remont-mobilnykh-telefonov
	// Which should be deleted because it became empty
	if _, err := os.Stat(filepath.Dir(savedSub.FilePath)); !os.IsNotExist(err) {
		t.Fatalf("Subcategory empty parent directory was not deleted: %s", filepath.Dir(savedSub.FilePath))
	}
	t.Log("Verification: Subcategory file and empty parent directory deleted.")
}
