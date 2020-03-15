package model

import "time"

type Classifieds struct {
	ID          uint      `gorm:"primary_key" json:"id"`
	Title       string    `json:"title"`
	Price       string    `json:"price"`
	Location    string    `json:"location"`
	Description string    `json:"description"`
	Url         string    `json:"url"`
	PublishedAt time.Time `json:"published_at"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
	DeletedAt   time.Time `json:"deleted_at"`
}

func (Classifieds) TableName() string { return "classifiedss" }
