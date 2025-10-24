package rabbitmq

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"time"

	amqp "github.com/rabbitmq/amqp091-go"
)

type Producer struct {
	conn    *amqp.Connection
	channel *amqp.Channel
	queue   string
}

// TelemetryEvent представляет событие телеметрии
type TelemetryEvent struct {
	DeviceID   string    `json:"device_id"`
	MetricName string    `json:"metric_name"`
	Value      float64   `json:"value"`
	Unit       string    `json:"unit"`
	Timestamp  time.Time `json:"timestamp"`
}

// NewProducer создает нового producer для RabbitMQ
func NewProducer(url string, queueName string) (*Producer, error) {
	// Подключение к RabbitMQ
	conn, err := amqp.Dial(url)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to RabbitMQ: %w", err)
	}

	// Создание канала
	channel, err := conn.Channel()
	if err != nil {
		conn.Close()
		return nil, fmt.Errorf("failed to open channel: %w", err)
	}

	// Объявление очереди
	_, err = channel.QueueDeclare(
		queueName, // название очереди
		true,      // durable (сохраняется при перезапуске)
		false,     // auto-delete
		false,     // exclusive
		false,     // no-wait
		nil,       // arguments
	)
	if err != nil {
		channel.Close()
		conn.Close()
		return nil, fmt.Errorf("failed to declare queue: %w", err)
	}

	log.Printf("✅ Connected to RabbitMQ, queue: %s", queueName)

	return &Producer{
		conn:    conn,
		channel: channel,
		queue:   queueName,
	}, nil
}

// PublishTelemetry отправляет событие телеметрии в RabbitMQ
func (p *Producer) PublishTelemetry(event TelemetryEvent) error {
	// Сериализация в JSON
	body, err := json.Marshal(event)
	if err != nil {
		return fmt.Errorf("failed to marshal event: %w", err)
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	// Отправка сообщения
	err = p.channel.PublishWithContext(
		ctx,
		"",      // exchange
		p.queue, // routing key (название очереди)
		false,   // mandatory
		false,   // immediate
		amqp.Publishing{
			DeliveryMode: amqp.Persistent, // сообщение сохраняется на диск
			ContentType:  "application/json",
			Body:         body,
			Timestamp:    time.Now(),
		},
	)
	if err != nil {
		return fmt.Errorf("failed to publish message: %w", err)
	}

	log.Printf("📤 Published telemetry: %s - %s = %.2f %s",
		event.DeviceID, event.MetricName, event.Value, event.Unit)

	return nil
}

// Close закрывает соединение с RabbitMQ
func (p *Producer) Close() {
	if p.channel != nil {
		p.channel.Close()
	}
	if p.conn != nil {
		p.conn.Close()
	}
	log.Println("🔌 RabbitMQ connection closed")
}