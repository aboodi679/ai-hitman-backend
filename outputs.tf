output "s3_bucket_name" {
  value = aws_s3_bucket.model_bucket.bucket
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.player_stats.name
}