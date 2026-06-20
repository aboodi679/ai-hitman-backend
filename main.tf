provider "aws" {
  region = var.aws_region
}

# ─────────────────────────────────────────────
# S3 Bucket — stores the RL model file
# ─────────────────────────────────────────────
resource "aws_s3_bucket" "model_bucket" {
  bucket        = var.bucket_name
  force_destroy = true

  tags = {
    Project = "hitman-fyp"
  }
}

resource "aws_s3_bucket_public_access_block" "model_bucket_block" {
  bucket                  = aws_s3_bucket.model_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# ─────────────────────────────────────────────
# DynamoDB Table — stores player session stats
# ─────────────────────────────────────────────
resource "aws_dynamodb_table" "player_stats" {
  name         = var.dynamodb_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "player_id"
  range_key    = "timestamp"

  attribute {
    name = "player_id"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  tags = {
    Project = "hitman-fyp"
  }
}