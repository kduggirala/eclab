if (!require("readxl")) install.packages("readxl")
if (!require("dplyr")) install.packages("dplyr")
if (!require("ggplot2")) install.packages("ggplot2")
if (!require("lubridate")) install.packages("lubridate")

library(readxl)
library(dplyr)
library(ggplot2)
library(lubridate)


setwd("~/Desktop/New Mexico Cannabis Revenue")
files <- list.files(pattern = "\\.xls[x]?$")

create_date <- function(filename) {
  parts <- strsplit(filename, "[_.]")[[1]]
  month_name <- parts[1]
  year <- parts[2]
  year <- as.numeric(gsub("\\.xls[x]?$", "", year))
  date_str <- paste0("01 ", month_name, " ", year)
  as.Date(date_str, format="%d %B %Y")
}

read_data <- function(file) {
  df <- read_excel(file)
  df$Date <- create_date(file)
  return(df)
}

data_list <- lapply(files, read_data)
combined_data <- bind_rows(data_list)

aggregated_data <- combined_data %>%
  group_by(Date) %>%
  summarise(MedicalSales = sum(`Medical Sales`, na.rm = TRUE),
            AdultUseSales = sum(`Adult-Use Sales`, na.rm = TRUE))

graph <- ggplot(aggregated_data, aes(x = Date)) +
  geom_line(aes(y = MedicalSales, color = "Medical Sales"), size = 1) +
  geom_line(aes(y = AdultUseSales, color = "Adult-Use Sales"), size = 1) +
  labs(title = "Cannabis Revenue over Time (NM)",
       subtitle = "Comparison of Medical Sales and Adult-Use Sales",
       x = "Date",
       y = "Revenue (USD)",
       caption = "Data Source: New Mexico Cannabis Revenue") +
  scale_x_date(date_breaks = "1 month", date_labels = "%b %Y") +
  scale_color_manual(values = c("Medical Sales" = "blue", "Adult-Use Sales" = "red")) +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(hjust = 0.5, size = 16, face = "bold"),
    plot.subtitle = element_text(hjust = 0.5, size = 14),
    plot.caption = element_text(hjust = 0, size = 8),
    axis.title = element_text(size = 12),
    axis.text = element_text(size = 10),
    legend.title = element_blank(),
    legend.position = "bottom",
    legend.text = element_text(size = 10)
  )
print(graph)
ggsave("Cannabis_Revenue_TSeries.png", plot = graph, path = getwd(), width = 11, height = 8.5, dpi = 300, units = "in")



total_medical_sales <- 0
total_adult_use_sales <- 0
total_all_sales <- 0
extract_totals <- function(file) {
  df <- read_excel(file)
  # Assume the first column is named 'Description'
  # Adjust the column name as per your actual data
  totals_row <- df %>% filter(grepl("Totals:", Licensee)) 
  if (nrow(totals_row) > 0) {
    total_medical_sales <<- total_medical_sales + totals_row$`Medical Sales`
    total_adult_use_sales <<- total_adult_use_sales + totals_row$`Adult-Use Sales`
    total_all_sales <<- total_all_sales + totals_row$`Total Sales`
  }
}
lapply(files, extract_totals)
average_medical_sales <- (total_medical_sales / total_all_sales) * 100
average_adult_use_sales <- (total_adult_use_sales / total_all_sales) * 100
sales_data <- data.frame(
  Category = c("Medical Sales", "Adult-Use Sales"),
  Average = c(average_medical_sales, average_adult_use_sales)
)
sales_data$label_position <- cumsum(sales_data$Average) - 0.5 * sales_data$Average
sales_data$label <- sprintf("%.1f%%", sales_data$Average)
pie_chart <- ggplot(sales_data, aes(x = "", y = Average, fill = Category)) +
  geom_bar(width = 1, stat = "identity") +
  coord_polar(theta = "y") +
  geom_text(aes(label = label, y = label_position), color = "white", size = 5) +
  labs(title = "Comparison of Average Medical vs Adult-Use Sales in New Mexico, 2022-Present",
       fill = "Category") +
  theme_minimal() +
  theme(axis.line = element_blank(),
        axis.text = element_blank(),
        axis.ticks = element_blank(),
        axis.title = element_blank(),
        panel.grid = element_blank(),
        plot.title = element_text(hjust = 0.5, size = 14, face = "bold"),
        legend.title = element_blank(),
        legend.position = "bottom",
        legend.text = element_text(size = 10)) +
  scale_fill_manual(values = c("Medical Sales" = "blue", "Adult-Use Sales" = "red"))

# Print the pie chart to the R plotting window
print(pie_chart)

# Export the pie chart as a high-quality PNG image
ggsave("NM_REVENUE_PIECHART.png", plot = pie_chart, path = getwd(), width = 8, height = 8, dpi = 300, units = "in")

