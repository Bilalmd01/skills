package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
	"os"
	"strings"
	"time"

	"github.com/TeneoProtocolAI/teneo-agent-sdk/pkg/agent"
	"github.com/joho/godotenv"
)

// ===============================
// Simple mapping IATA -> city name (for weather lookup)
// ===============================
var airportCityMap = map[string]string{
	"CGK": "Jakarta",
	"DPS": "Denpasar",
	"SUB": "Surabaya",
	"BDO": "Bandung",
	"SIN": "Singapore",
	"KUL": "Kuala Lumpur",
	"BKK": "Bangkok",
	"HND": "Tokyo",
	"NRT": "Tokyo",
	"KIX": "Osaka",
	"LAX": "Los Angeles",
	"JFK": "New York",
	"CDG": "Paris",
	"FRA": "Frankfurt",
	"DXB": "Dubai",
	"SYD": "Sydney",
}

// ===============================
// Agent Struct
// ===============================
type SarqovikAgent006Agent struct{}

// ===============================
// ProcessTask (Command Router)
// ===============================
func (a *SarqovikAgent006Agent) ProcessTask(ctx context.Context, task string) (string, error) {
	log.Printf("Processing task: %s", task)

	// Clean & normalize
	task = strings.TrimSpace(task)
	task = strings.TrimPrefix(task, "/")

	if task == "" {
		return helpMessage(), nil
	}

	originalTask := task
	taskLower := strings.ToLower(task)
	parts := strings.Fields(taskLower)
	if len(parts) == 0 {
		return helpMessage(), nil
	}

	command := parts[0]
	args := parts[1:]

	switch command {

	case "visa_info":
		if len(args) < 2 {
			return "Usage: visa_info [nationality] [destination]\nExample: visa_info Indonesian Japan", nil
		}
		prompt := fmt.Sprintf(
			"You are an expert on global travel visa requirements.\nUser query: %s\n\nExplain visa rules (visa-free, visa-on-arrival, eVisa, or embassy visa), including basic stay duration and important notes. Be concise and clear.",
			originalTask,
		)
		return a.askAI(ctx, prompt)

	case "convert_currency":
		if len(args) < 3 {
			return "Usage: convert_currency [amount] [from] [to]\nExample: convert_currency 200 USD to IDR", nil
		}
		prompt := fmt.Sprintf(
			"You are a currency conversion assistant.\nUser query: %s\n\nProvide an estimated real-time conversion and mention that exact values may vary slightly by provider.",
			originalTask,
		)
		return a.askAI(ctx, prompt)

	case "airport_status":
		if len(args) < 1 {
			return "Usage: airport_status [IATA_code]\nExample: airport_status CGK", nil
		}

		iata := strings.ToUpper(args[0])

		// 1) Real-time weather
		weatherText, wErr := getAirportWeather(ctx, iata)
		if wErr != nil {
			log.Printf("Weather lookup failed for %s: %v", iata, wErr)
			weatherText = "Real-time weather data is currently unavailable."
		}

		// 2) Real-time flight status (recent departures)
		flightText, fErr := getAirportFlightStatus(ctx, iata)
		if fErr != nil {
			log.Printf("Flight status lookup failed for %s: %v", iata, fErr)
			flightText = "Real-time flight status data is currently unavailable."
		}

		// 3) AI summary with context
		prompt := fmt.Sprintf(
			"You are an airport status and travel assistant.\n\nUser query: %s\n\nHere is live context for airport %s:\n\n[Weather]\n%s\n\n[Recent Flight Status]\n%s\n\nUsing this context, give a concise, practical summary about current airport conditions, possible delays, and travel tips. If live flight delay data isn't complete, be honest and rely on the given context plus general travel best practices.",
			originalTask,
			iata,
			weatherText,
			flightText,
		)

		aiAnswer, aiErr := a.askAI(ctx, prompt)
		if aiErr != nil {
			return fmt.Sprintf(
				"%s\n\n%s\n\n(Additional AI summary is temporarily unavailable: %v)",
				weatherText,
				flightText,
				aiErr,
			), nil
		}

		return fmt.Sprintf("%s\n\n%s\n\n%s", weatherText, flightText, aiAnswer), nil

	case "events_in":
		if len(args) < 1 {
			return "Usage: events_in [city] [month]\nExample: events_in Tokyo March", nil
		}
		prompt := fmt.Sprintf(
			"You are a global events guide.\nUser query: %s\n\nSuggest popular events, festivals, concerts, or cultural activities for this city and month. If the month is not provided, use the nearest upcoming months.",
			originalTask,
		)
		return a.askAI(ctx, prompt)

	case "cultural_tips":
		if len(args) < 1 {
			return "Usage: cultural_tips [destination]\nExample: cultural_tips South Korea", nil
		}
		prompt := fmt.Sprintf(
			"You are a cultural etiquette expert.\nUser query: %s\n\nProvide cultural dos and don'ts, greetings, politeness rules, and taboos for this destination.",
			originalTask,
		)
		return a.askAI(ctx, prompt)

	case "emergency_info":
		if len(args) < 1 {
			return "Usage: emergency_info [country]\nExample: emergency_info Japan", nil
		}
		prompt := fmt.Sprintf(
			"You are a safety and emergency contact advisor.\nUser query: %s\n\nList important emergency numbers for this country (police, ambulance, fire) and any useful traveler hotlines. If exact numbers are uncertain, say so and provide best-known or typical patterns.",
			originalTask,
		)
		return a.askAI(ctx, prompt)

	case "best_time_to_visit":
		if len(args) < 1 {
			return "Usage: best_time_to_visit [destination]\nExample: best_time_to_visit Bali", nil
		}
		prompt := fmt.Sprintf(
			"You are a seasonal travel advisor.\nUser query: %s\n\nExplain the best time to visit this destination, including weather, peak vs low season, price trends, and any special events.",
			originalTask,
		)
		return a.askAI(ctx, prompt)

	case "stay_finder":
		if len(args) < 1 {
			return "Usage: stay_finder [destination] [budget] [guests]\nExample: stay_finder Singapore 500000 2", nil
		}
		prompt := fmt.Sprintf(
			"You are a stay recommendation engine.\nUser query: %s\n\nSuggest types of stays (hotel, hostel, homestay, Airbnb-style) with budget tiers and recommended neighborhoods. Be practical and structured.",
			originalTask,
		)
		return a.askAI(ctx, prompt)

	case "hidden_gems":
		if len(args) < 1 {
			return "Usage: hidden_gems [destination]\nExample: hidden_gems Bangkok", nil
		}
		prompt := fmt.Sprintf(
			"You are a hidden gem and local secret spot expert.\nUser query: %s\n\nRecommend non-touristy spots, local hangouts, scenic viewpoints, and unique experiences for this destination.",
			originalTask,
		)
		return a.askAI(ctx, prompt)

	case "food_recommend":
		if len(args) < 1 {
			return "Usage: food_recommend [destination]\nExample: food_recommend Seoul", nil
		}
		prompt := fmt.Sprintf(
			"You are a local food and restaurant guide.\nUser query: %s\n\nSuggest signature dishes, must-try restaurants, street food areas, and local specialties for this destination.",
			originalTask,
		)
		return a.askAI(ctx, prompt)

	default:
		return fmt.Sprintf(
			"Unknown command '%s'. Available commands: visa_info, convert_currency, airport_status, events_in, cultural_tips, emergency_info, best_time_to_visit, stay_finder, hidden_gems, food_recommend",
			command,
		), nil
	}
}

// ===============================
// AI Backend (OpenAI-compatible)
// ===============================
func (a *SarqovikAgent006Agent) askAI(ctx context.Context, prompt string) (string, error) {
	apiKey := os.Getenv("OPENAI_API_KEY")
	if apiKey == "" {
		return "", fmt.Errorf("OPENAI_API_KEY is not set in .env")
	}

	baseURL := os.Getenv("OPENAI_BASE_URL")
	if baseURL == "" {
		baseURL = "https://api.openai.com/v1"
	}
	baseURL = strings.TrimRight(baseURL, "/")

	model := os.Getenv("OPENAI_MODEL")
	if model == "" {
		model = "gpt-4.1-mini"
	}

	systemMsg := `You are GlobePilot AI Agent, an intelligent travel assistant.
You answer with accurate, practical, and concise information.
Whenever possible, respond in the same language as the user's query.
You specialize in: visas, currency, airports, events, culture, safety, accommodations, hidden gems, and local food.`

	body := map[string]interface{}{
		"model": model,
		"messages": []map[string]string{
			{"role": "system", "content": systemMsg},
			{"role": "user", "content": prompt},
		},
		"temperature": 0.4,
	}

	data, err := json.Marshal(body)
	if err != nil {
		return "", err
	}

	req, err := http.NewRequestWithContext(
		ctx,
		http.MethodPost,
		fmt.Sprintf("%s/chat/completions", baseURL),
		bytes.NewReader(data),
	)
	if err != nil {
		return "", err
	}

	req.Header.Set("Authorization", "Bearer "+apiKey)
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{Timeout: 25 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	raw, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	if resp.StatusCode >= 300 {
		log.Printf("❌ AI API error: %s - %s", resp.Status, string(raw))
		return "", fmt.Errorf("AI API error: %s", resp.Status)
	}

	var parsed struct {
		Choices []struct {
			Message struct {
				Content string `json:"content"`
			} `json:"message"`
		} `json:"choices"`
	}

	if err := json.Unmarshal(raw, &parsed); err != nil {
		return "", fmt.Errorf("failed to parse AI response: %w", err)
	}
	if len(parsed.Choices) == 0 {
		return "", fmt.Errorf("no AI response")
	}

	return strings.TrimSpace(parsed.Choices[0].Message.Content), nil
}

// ===============================
// Real-time Weather (OpenWeatherMap)
// ===============================
func getAirportWeather(ctx context.Context, iata string) (string, error) {
	apiKey := os.Getenv("OPENWEATHER_API_KEY")
	if apiKey == "" {
		return "", fmt.Errorf("OPENWEATHER_API_KEY is not set")
	}

	iata = strings.ToUpper(strings.TrimSpace(iata))

	city, ok := airportCityMap[iata]
	if !ok {
		city = iata
	}

	units := os.Getenv("OPENWEATHER_UNITS")
	if units == "" {
		units = "metric"
	}

	q := url.Values{}
	q.Set("q", city)
	q.Set("appid", apiKey)
	q.Set("units", units)

	endpoint := "https://api.openweathermap.org/data/2.5/weather?" + q.Encode()

	req, err := http.NewRequestWithContext(ctx, http.MethodGet, endpoint, nil)
	if err != nil {
		return "", err
	}

	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	raw, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	if resp.StatusCode >= 300 {
		return "", fmt.Errorf("weather API error: %s - %s", resp.Status, string(raw))
	}

	var data struct {
		Name    string `json:"name"`
		Main    struct {
			Temp     float64 `json:"temp"`
			Humidity int     `json:"humidity"`
		} `json:"main"`
		Weather []struct {
			Description string `json:"description"`
		} `json:"weather"`
	}

	if err := json.Unmarshal(raw, &data); err != nil {
		return "", fmt.Errorf("failed to parse weather response: %w", err)
	}

	if data.Name == "" {
		data.Name = city
	}

	desc := "unknown"
	if len(data.Weather) > 0 {
		desc = data.Weather[0].Description
	}

	unitSymbol := "°C"
	if units == "imperial" {
		unitSymbol = "°F"
	}

	return fmt.Sprintf(
		"Current weather near %s (%s): %.1f%s, %s, humidity %d%%",
		data.Name,
		iata,
		data.Main.Temp,      // ⬅️ pakai data.Main.Temp
		unitSymbol,
		desc,
		data.Main.Humidity,  // ⬅️ pakai data.Main.Humidity
	), nil
}

// ===============================
// Real-time Flight Status (AviationStack)
// ===============================
func getAirportFlightStatus(ctx context.Context, iata string) (string, error) {
	provider := strings.ToLower(os.Getenv("FLIGHT_STATUS_PROVIDER"))
	if provider == "" {
		provider = "aviationstack"
	}

	switch provider {
	case "aviationstack":
		return getFlightStatusAviationStack(ctx, iata)
	default:
		return "", fmt.Errorf("unknown FLIGHT_STATUS_PROVIDER: %s (supported: aviationstack)", provider)
	}
}

func getFlightStatusAviationStack(ctx context.Context, iata string) (string, error) {
	apiKey := os.Getenv("AVIATIONSTACK_API_KEY")
	if apiKey == "" {
		return "", fmt.Errorf("AVIATIONSTACK_API_KEY is not set")
	}

	iata = strings.ToUpper(strings.TrimSpace(iata))

	q := url.Values{}
	q.Set("access_key", apiKey)
	q.Set("dep_iata", iata)
	q.Set("limit", "5")

	endpoint := "http://api.aviationstack.com/v1/flights?" + q.Encode()

	req, err := http.NewRequestWithContext(ctx, http.MethodGet, endpoint, nil)
	if err != nil {
		return "", err
	}

	client := &http.Client{Timeout: 15 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	raw, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	if resp.StatusCode >= 300 {
		return "", fmt.Errorf("flight API error: %s - %s", resp.Status, string(raw))
	}

	var data struct {
		Data []struct {
			Airline struct {
				Name string `json:"name"`
			} `json:"airline"`
			Flight struct {
				Iata string `json:"iata"`
			} `json:"flight"`
			Departure struct {
				Airport   string `json:"airport"`
				Iata      string `json:"iata"`
				Scheduled string `json:"scheduled"`
				Actual    string `json:"actual"`
			} `json:"departure"`
			Arrival struct {
				Airport   string `json:"airport"`
				Iata      string `json:"iata"`
				Scheduled string `json:"scheduled"`
				Actual    string `json:"actual"`
			} `json:"arrival"`
			FlightStatus string `json:"flight_status"`
		} `json:"data"`
	}

	if err := json.Unmarshal(raw, &data); err != nil {
		return "", fmt.Errorf("failed to parse flight status response: %w", err)
	}

	if len(data.Data) == 0 {
		return "No recent departure flight data available for this airport.", nil
	}

	var b strings.Builder
	b.WriteString(fmt.Sprintf("Recent departure flights for %s:\n", iata))

	for i, f := range data.Data {
		if i >= 5 {
			break
		}
		airline := f.Airline.Name
		if airline == "" {
			airline = "Unknown airline"
		}
		flightCode := f.Flight.Iata
		if flightCode == "" {
			flightCode = "N/A"
		}

		depTime := shortTimeFromISO(f.Departure.Scheduled)
		arrAirport := f.Arrival.Airport
		if arrAirport == "" {
			arrAirport = f.Arrival.Iata
		}
		if arrAirport == "" {
			arrAirport = "Unknown destination"
		}

		status := f.FlightStatus
		if status == "" {
			status = "unknown"
		}

		b.WriteString(fmt.Sprintf(
			"• %s %s → %s | status: %s | sched: %s\n",
			airline, flightCode, arrAirport, status, depTime,
		))
	}

	return strings.TrimSpace(b.String()), nil
}

func shortTimeFromISO(ts string) string {
	if ts == "" {
		return "N/A"
	}
	t, err := time.Parse(time.RFC3339, ts)
	if err != nil {
		if t2, err2 := time.Parse("2006-01-02T15:04:05-07:00", ts); err2 == nil {
			return t2.Format("15:04")
		}
		return ts
	}
	return t.Format("15:04")
}

// ===============================
// Help Message
// ===============================
func helpMessage() string {
	return `Available commands:
- visa_info [nationality] [destination]
- convert_currency [amount] [from] [to]
- airport_status [IATA_code]
- events_in [city] [month]
- cultural_tips [destination]
- emergency_info [country]
- best_time_to_visit [destination]
- stay_finder [destination] [budget] [guests]
- hidden_gems [destination]
- food_recommend [destination]`
}

// ===============================
// main()
// ===============================
func main() {
	_ = godotenv.Load()

	config := agent.DefaultConfig()

	config.Name = "GlobePilot AI Agent 2"
	config.Description = `GlobePilot AI Agent is a next-generation travel assistant designed to deliver a smarter, faster, and more personalized travel experience.
Powered by AI-driven analysis and real-time global data, GlobePilot AI helps travelers discover top destinations, recommended activities, transport options, and accurate trip cost estimates — all through a simple conversation.

Built as an intuitive travel companion, GlobePilot AI doesn’t just answer questions; it understands the user’s travel style.
Whether you’re a solo traveler, backpacker, or luxury explorer, this agent can provide highly relevant, accurate, and practical suggestions.

From finding the cheapest flight deals, checking airport status, comparing hotels, building a full itinerary, to uncovering the best local food — GlobePilot AI acts as a smart navigator that assists your journey from start to finish.

With a wide range of intelligent modules such as Destination Guide, Trip Recommender, Food Explorer, Visa Checker, Currency Converter, and many more, GlobePilot AI becomes the most complete travel companion you’ve ever had.`

	config.Capabilities = []string{
		"visa_requirement_checker",
		"currency_conversion_service",
		"airport_status_monitor",
		"global_event_discovery",
		"cultural_etiquette_guide",
		"emergency_contact_provider",
		"seasonal_travel_advisor",
		"stay_recommendation_engine",
		"hidden_gem_finder",
		"local_food_explorer",
	}

	config.PrivateKey = os.Getenv("PRIVATE_KEY")
	config.NFTTokenID = os.Getenv("NFT_TOKEN_ID")
	config.OwnerAddress = os.Getenv("OWNER_ADDRESS")

	enhancedAgent, err := agent.NewEnhancedAgent(&agent.EnhancedAgentConfig{
		Config:       config,
		AgentHandler: &SarqovikAgent006Agent{},
	})
	if err != nil {
		log.Fatal(err)
	}

	log.Println("Starting GlobePilot AI Agent 2...")
	log.Printf("Capabilities: %v", config.Capabilities)
	enhancedAgent.Run()
}
